import copy
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
import frozendict
import typing

from d3m import container
from d3m.base import utils
from d3m.container import DataFrame as d3m_DataFrame
from d3m.metadata import base as mbase
from d3m.metadata import hyperparams, params
from d3m.primitive_interfaces.base import CallResult
from d3m.primitive_interfaces.unsupervised_learning import UnsupervisedLearnerPrimitiveBase
from . import config

Input = container.DataFrame
Output = container.DataFrame


class Params(params.Params):
    mapping: typing.Dict
    all_columns: typing.Set[str]
    empty_columns: typing.List[object]
    textmapping: typing.Dict
    requirement: typing.Dict
    cat_columns: typing.List[object]
    cat_col_index: typing.List[object]


class UEncHyperparameter(hyperparams.Hyperparams):
    text2int = hyperparams.UniformBool(
        default=False,
        description='Whether to convert everything to numerical. For text columns, each row may get converted into a column',
        semantic_types=['http://schema.org/Boolean',
                        'https://metadata.datadrivendiscovery.org/types/ControlParameter'])

    use_columns = hyperparams.Set(
        elements=hyperparams.Hyperparameter[int](-1),
        default=(),
        semantic_types=['https://metadata.datadrivendiscovery.org/types/ControlParameter'],
        description="A set of column indices to force primitive to operate on. If any specified column cannot be parsed, it is skipped.",
    )
    exclude_columns = hyperparams.Set(
        elements=hyperparams.Hyperparameter[int](-1),
        default=(),
        semantic_types=['https://metadata.datadrivendiscovery.org/types/ControlParameter'],
        description="A set of column indices to not operate on. Applicable only if \"use_columns\" is not provided.",
    )
    return_result = hyperparams.Enumeration(
        values=['append', 'replace', 'new'],
        default='replace',
        semantic_types=['https://metadata.datadrivendiscovery.org/types/ControlParameter'],
        description="Should parsed columns be appended, should they replace original columns, or should only parsed columns be returned? This hyperparam is ignored if use_semantic_types is set to false.",
    )
    use_semantic_types = hyperparams.UniformBool(
        default=False,
        semantic_types=['https://metadata.datadrivendiscovery.org/types/ControlParameter'],
        description="Controls whether semantic_types metadata will be used for filtering columns in input dataframe. Setting this to false makes the code ignore return_result and will produce only the output dataframe"
    )
    add_index_columns = hyperparams.UniformBool(
        default=True,
        semantic_types=['https://metadata.datadrivendiscovery.org/types/ControlParameter'],
        description="Also include primary index columns if input data has them. Applicable only if \"return_result\" is set to \"new\".",
    )


## reference: https://github.com/scikit-learn/scikit-learn/issues/8136
class Label_encoder(object):
    def __init__(self):
        self.class_index = None

    def fit_pd(self, df, cols=[]):
        '''
        fit all columns in the df or specific list.
        generate a dict:
        {feature1:{label1:1,label2:2}, feature2:{label1:1,label2:2}...}
        '''
        if len(cols) == 0:
            cols = df.columns
        self.class_index = {}
        for f in cols:
            uf = df[f].unique()
            self.class_index[f] = {}
            index = 1
            for item in uf:
                self.class_index[f][item] = index
                index += 1

    def transform_pd(self, df, cols=[]):
        '''
        transform all columns in the df or specific list from lable to index, return and update dataframe.
        '''
        newdf = copy.deepcopy(df)
        if len(cols) == 0:
            cols = df.columns
        for f in cols:
            if f in self.class_index:
                newdf[f] = df[f].apply(lambda d: self.__update_label(f, d))
        return newdf

    def get_params(self):
        return self.class_index

    def set_params(self, textmapping):
        self.class_index = textmapping

    def __update_label(self, f, x):
        '''
        update the label to index, if not found in the dict, add and update the dict.
        '''
        try:
            return self.class_index[f][x]
        except:
            self.class_index[f][x] = max(self.class_index[f].values()) + 1
            return self.class_index[f][x]


class UnaryEncoder(UnsupervisedLearnerPrimitiveBase[Input, Output, Params, UEncHyperparameter]):
    """
    A primitive which converts the numerical attributes to multi-column attributes.
    Each new column value would be 1 if the original value is larger than this column's name value
    Otherwise the new column value would be 0
    This encoder only operate when the amount of the numerical data is less than 12, otherwise the column would keep unchanged.
    """
    metadata = hyperparams.base.PrimitiveMetadata({
        "id": "DSBox-unary-encoder",
        "version": config.VERSION,
        "name": "DSBox Unary Data Encoder",
        "description": "Encode using unary code for orinal data",
        "python_path": "d3m.primitives.data_transformation.unary_encoder.DSBOX",
        "primitive_family": "DATA_TRANSFORMATION",
        "algorithm_types": ["ENCODE_ONE_HOT"],
        "source": {
            "name": config.D3M_PERFORMER_TEAM,
            "contact": config.D3M_CONTACT,
            "uris": [config.REPOSITORY]
        },
        ### Automatically generated
        # "primitive_code"
        # "original_python_path"
        # "schema"
        # "structural_type"
        ### Optional
        "keywords": ["preprocessing", "encoding"],
        "installation": [config.INSTALLATION],
        # "location_uris": [],
        # "precondition": [],
        # "effects": [],
        # "hyperparms_to_tune": []
    })

    def __repr__(self):
        return "%s(%r)" % ('UnaryEncoder', self.__dict__)

    def __init__(self, *, hyperparams: UEncHyperparameter) -> None:
        super().__init__(hyperparams=hyperparams)

        self.hyperparams = hyperparams
        self._text2int = hyperparams['text2int']
        self._textmapping: typing.Dict = dict()
        self._mapping: typing.Dict = dict()
        self._all_columns: typing.Set = set()
        self._empty_columns: typing.List[object] = []
        self._cat_col_index: typing.List[object] = []
        self._cat_columns: typing.List[object] = []
        self._training_inputs = None
        self._fitted = False
        self._col_index = None
        self._requirement: typing.Dict = dict()

    def get_params(self) -> Params:

        # Hack to work around pytypes bug. Covert numpy int64 to int.
        for key in self._mapping.keys():
            self._mapping[key] = [np.nan if np.isnan(x) else int(x) for x in self._mapping[key]]

        param = Params(mapping=self._mapping,
                       all_columns=self._all_columns,
                       empty_columns=self._empty_columns,
                       textmapping=self._textmapping,
                       requirement=self._requirement,
                       cat_columns=self._cat_columns,
                       cat_col_index=self._cat_col_index
                       )
        return param

    def set_params(self, *, params: Params) -> None:
        self._textmapping = params['textmapping']
        self._mapping = params['mapping']
        self._all_columns = params['all_columns']
        self._empty_columns = params['empty_columns']
        self._requirement = params['requirement']
        self._cat_columns = params['cat_columns']
        self._cat_col_index = params['cat_col_index']
        self._fitted = True

    def set_training_data(self, *, inputs: Input) -> None:
        self._training_inputs = inputs
        self._fitted = False

    def fit(self, *, timeout: float = None, iterations: int = None) -> CallResult[None]:
        """
        Need training data from set_training_data first.
        The encoder would record specified columns to encode and column values to
        unary encode later in the produce step.
        """
        if self._fitted:
            return CallResult(None)

        if self._training_inputs is None:
            raise ValueError('Missing training(fitting) data.')

        data = self._training_inputs.copy()
        all_attributes = data.metadata.list_columns_with_semantic_types(semantic_types=[
            "https://metadata.datadrivendiscovery.org/types/Attribute"])

        # Remove columns with all empty values, structural type str
        numeric = data.metadata.list_columns_with_semantic_types(['http://schema.org/Integer', 'http://schema.org/Float'])
        numeric = [x for x in numeric if x in all_attributes]
        for element in numeric:
            if data.metadata.query((mbase.ALL_ELEMENTS, element)).get('structural_type', ()) == str:
                if pd.isnull(pd.to_numeric(data.iloc[:, element], errors='coerce')).sum() == data.shape[0]:
                    self._empty_columns.append(element)

        # Remove columns with all empty values, structural numeric
        is_empty = pd.isnull(data).sum(axis=0) == data.shape[0]
        for i in all_attributes:
            if is_empty.iloc[i]:
                self._empty_columns.append(i)
        self._empty_columns = list(set(self._empty_columns))
        self._empty_columns.reverse()
        self._empty_columns = container.List(self._empty_columns)
        data = data.remove_columns(self._empty_columns)
        # print('fit', data.shape)

        categorical_attributes = data.metadata.list_columns_with_semantic_types(
            semantic_types=[
                "https://metadata.datadrivendiscovery.org/types/OrdinalData",
                "https://metadata.datadrivendiscovery.org/types/CategoricalData"
            ]
        )
        all_attributes = data.metadata.list_columns_with_semantic_types(
            semantic_types=["https://metadata.datadrivendiscovery.org/types/Attribute"]
        )
        self._cat_col_index = container.List(set(all_attributes).intersection(numeric))
        self._cat_columns = container.List(data.columns[self._cat_col_index].tolist())
        # import pdb
        # pdb.set_trace()
        numerical_values = data.iloc[:, self._cat_col_index].apply(
            lambda col: pd.to_numeric(col, errors='coerce'))

        self._all_columns = set(data.columns)

        # mapping
        idict = {}
        for name in self._cat_columns:
            col = numerical_values[name]
            idict[name] = sorted(col.unique())
        self._mapping = idict

        if self._text2int:
            texts = data.drop(self._mapping.keys(), axis=1)
            texts = texts.select_dtypes(include=[object])
            le = Label_encoder()
            le.fit_pd(texts)
            self._textmapping = le.get_params()

        # determine whether to run unary encoder on the given column or not
        data_enc = data.iloc[:, self._cat_col_index].apply(lambda col: pd.to_numeric(col, errors='coerce'))
        for column_name in data_enc:
            col = data_enc[column_name]
            col.is_copy = False
            # only apply unary encoder when the amount of the numerical data is less than 12
            if col.unique().shape[0] < 13:
                self._requirement[column_name] = True
            else:
                self._requirement[column_name] = False

        self._fitted = True

        return CallResult(None, has_finished=True, iterations_done=1)

    def __encode_column(self, col):
        unary = pd.DataFrame(col)
        for v in self._mapping[col.name]:
            unary[col.name + "_" + str(v)] = (col >= v).astype(int)
        return unary.drop(col.name, axis=1)

    def produce(self, *, inputs: Input, timeout: float = None, iterations: int = None) -> CallResult[Output]:
        """
        Convert and output the input data into unary encoded format,
        using the trained (fitted) encoder.
        Value unseen in training_inputs would be rounded to nearest value in training_inputs.
        Missing(NaN) cells in a column one-hot encoded would give
        out a row of all-ZERO columns for the target column.
        """
        # if self._target_columns == []:
        #    return CallResult(inputs, True, 1)
        if not self._fitted:
            raise ValueError('Encoder model not fitted. Use fit()')

        # Return if there is nothing to encode
        if len(self._cat_columns) == 0:
            return CallResult(inputs, True, 1)

        if isinstance(inputs, pd.DataFrame):
            data = inputs.copy()
        else:
            data = inputs[0].copy()
        data = data.remove_columns(self._empty_columns)
        set_columns = set(data.columns)

        if set_columns != self._all_columns:
            raise ValueError('Columns(features) fed at produce() differ from fitted data.')

        # core part: encode the unary columns
        data_enc = data.iloc[:, self._cat_col_index].apply(lambda col: pd.to_numeric(col, errors='coerce'))
        data_else = data.drop(self._mapping.keys(), axis=1)
        res = []
        for column_name in data_enc:
            col = data_enc[column_name]
            col.is_copy = False
            # only apply unary encoder when the amount of the numerical data is less than 12
            if self._requirement[column_name]:
                chg_v = lambda x: min(self._mapping[col.name], key=lambda a: abs(a - x)) if x is not None else x
                # only encode the values which is not null
                col[col.notnull()] = col[col.notnull()].apply(chg_v)
                encoded = self.__encode_column(col)
                res.append(encoded)
            else:
                res.append(col)

        if self._text2int:
            texts = data_else.select_dtypes([object])
            le = Label_encoder()
            le.set_params(self._textmapping)
            data_else[texts.columns] = le.transform_pd(texts)
        # transfer the encoded results to dataFrame
        encoded = d3m_DataFrame(pd.concat(res, axis=1))
        # update dimensional information
        encoded.metadata = encoded.metadata.update((), inputs.metadata.query(()))
        columns_query = dict(inputs.metadata.query((mbase.ALL_ELEMENTS,)))
        new_dimension_data = dict(columns_query['dimension'])
        new_dimension_data['length'] = encoded.shape[1]
        columns_query['dimension'] = frozendict.FrozenOrderedDict(new_dimension_data)
        encoded.metadata = encoded.metadata.update((mbase.ALL_ELEMENTS,), frozendict.FrozenOrderedDict(columns_query))

        # update metadata for existing columns
        for index in range(len(encoded.columns)):
            old_metadata = dict(encoded.metadata.query((mbase.ALL_ELEMENTS, index)))
            old_metadata["structural_type"] = int
            old_metadata["semantic_types"] = (
                'http://schema.org/Integer', 'https://metadata.datadrivendiscovery.org/types/Attribute')
            encoded.metadata = encoded.metadata.update((mbase.ALL_ELEMENTS, index), old_metadata)
        # after extracting the traget columns, remove these columns from dataFrame
        data_else = data.remove_columns(self._cat_col_index)
        result = data_else.horizontal_concat(encoded)

        return CallResult(result, True, 1)

    @classmethod
    def _get_columns_to_fit(cls, inputs: Input, hyperparams: UEncHyperparameter):
        if not hyperparams['use_semantic_types']:
            return inputs, list(range(len(inputs.columns)))

        inputs_metadata = inputs.metadata

        def can_produce_column(column_index: int) -> bool:
            return cls._can_produce_column(inputs_metadata, column_index, hyperparams)

        columns_to_produce, columns_not_to_produce = utils.get_columns_to_use(
            metadata=inputs_metadata,
            use_columns=hyperparams['use_columns'], exclude_columns=hyperparams['exclude_columns'],
            can_use_column=can_produce_column)
        return inputs.iloc[:, columns_to_produce], columns_to_produce

    @classmethod
    def _can_produce_column(cls, inputs_metadata: mbase.DataMetadata, column_index: int, hyperparams: UEncHyperparameter) -> bool:
        column_metadata = inputs_metadata.query((mbase.ALL_ELEMENTS, column_index))

        semantic_types = column_metadata.get('semantic_types', [])
        if len(semantic_types) == 0:
            cls.logger.warning("No semantic types found in column metadata")
            return False
        if "https://metadata.datadrivendiscovery.org/types/Attribute" in semantic_types:
            return True

        return False
