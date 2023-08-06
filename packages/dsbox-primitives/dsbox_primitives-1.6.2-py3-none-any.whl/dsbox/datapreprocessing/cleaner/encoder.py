import logging
import typing
import re

import frozendict  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore

from d3m import container
from d3m.base import utils
from d3m.metadata import hyperparams, params
import d3m.metadata.base as mbase
from d3m.metadata.base import DataMetadata
from d3m.metadata.hyperparams import UniformInt
from d3m.primitive_interfaces.base import CallResult
from d3m.primitive_interfaces.unsupervised_learning import UnsupervisedLearnerPrimitiveBase

from . import config

Input = container.DataFrame
Output = container.DataFrame


class EncParams(params.Params):
    mapping: typing.Dict
    cat_columns: typing.List[str]
    empty_columns: typing.List[int]


class EncHyperparameter(hyperparams.Hyperparams):
    n_limit = UniformInt(lower=0, upper=100, default=12,
                         description='Limits the maximum number of columns generated from a single categorical column',
                         semantic_types=['http://schema.org/Integer',
                                         'https://metadata.datadrivendiscovery.org/types/TuningParameter'])
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


class Encoder(UnsupervisedLearnerPrimitiveBase[Input, Output, EncParams, EncHyperparameter]):
    """
    A robust one-hot encoder. Missing values are encoded as an additional column. Use hyperparamter n_limit to limit the
    maximum number of column generated. If n_limit>0, then only the top n_limit most frequent values are encoded into
    columns. the rest of the values are encoded into a single column."
    """
    metadata = hyperparams.base.PrimitiveMetadata({
        "id": "18f0bb42-6350-3753-8f2d-d1c3da70f279",
        "version": config.VERSION,
        "name": "ISI DSBox Data Encoder",
        "description": "Encode data, such as one-hot encoding for categorical data",
        "python_path": "d3m.primitives.data_transformation.encoder.DSBOX",
        "primitive_family": "DATA_TRANSFORMATION",
        "algorithm_types": ["ENCODE_ONE_HOT"],
        "source": {
            "name": config.D3M_PERFORMER_TEAM,
            "contact": config.D3M_CONTACT,
            "uris": [config.REPOSITORY]
        },
        "keywords": ["preprocessing", "encoding"],
        "installation": [config.INSTALLATION],
    })

    def __repr__(self):
        return "%s(%r)" % ('Encoder', self.__dict__)

    def __init__(self, *, hyperparams: EncHyperparameter) -> None:

        super().__init__(hyperparams=hyperparams)
        self.hyperparams = hyperparams
        self._mapping: typing.Dict = {}
        self._input_data: Input = None
        self._input_data_copy: Input = None
        self._fitted: bool = False
        self._cat_columns: typing.List[str] = []
        # self._col_index = None
        self._empty_columns: typing.List[str] = []
        self.logger = logging.getLogger(__name__)

    def set_training_data(self, *, inputs: Input) -> None:
        self._input_data = inputs
        self._fitted = False

    def _trim_features(self, feature, n_limit):

        topn = feature.dropna().unique()
        if n_limit:
            if feature.dropna().nunique() > n_limit:
                topn = list(feature.value_counts().head(n_limit).index)
                topn.append('other_')
        topn = [x for x in topn if x]
        return feature.name, topn

    def _remove_trailing_zeros(self, col_names):
        """
        Removes '.0' from the end of each column name in `col_names`.
        """
        return [re.sub('.0$', '', col_name) for col_name in col_names]

    def fit(self, *, timeout: float = None, iterations: int = None) -> CallResult[None]:

        if self._fitted:
            return CallResult(None)

        if self._input_data is None:
            raise ValueError('Missing training(fitting) data.')

        # Look at attribute columns only
        # print('fit in', self._input_data.columns)
        data = self._input_data.copy()
        all_attributes = DataMetadata.list_columns_with_semantic_types(data.metadata, semantic_types=[
            "https://metadata.datadrivendiscovery.org/types/Attribute"])

        # Remove columns with all empty values, structural type str
        numeric = DataMetadata.list_columns_with_semantic_types(
            data.metadata, ['http://schema.org/Integer', 'http://schema.org/Float'])
        numeric = [x for x in numeric if x in all_attributes]

        self._empty_columns = []
        self.logger.debug(f'Numeric columns: {numeric}')
        for element in numeric:
            if data.metadata.query((mbase.ALL_ELEMENTS, element)).get('structural_type', ()) == str:
                if pd.isnull(pd.to_numeric(data.iloc[:, element])).sum() == data.shape[0]:
                    self.logger.debug(f'Empty numeric str column: {element}')
                    self._empty_columns.append(element)

        # Remove columns with all empty values, structural numeric
        is_empty = pd.isnull(data).sum(axis=0) == data.shape[0]
        for i in all_attributes:
            if is_empty.iloc[i] and i not in self._empty_columns:
                self.logger.debug(f'Empty numeric str column: {element}')
                self._empty_columns.append(i)

        self.logger.debug('Removing entirely empty columns: {}'.format(data.columns[self._empty_columns]))

        data = container.DataFrame.remove_columns(data, self._empty_columns)

        categorical_attributes = DataMetadata. \
            list_columns_with_semantic_types(data.metadata,
                                             semantic_types=[
                                                 "https://metadata.datadrivendiscovery.org/types/OrdinalData",
                                                 "https://metadata.datadrivendiscovery.org/types/CategoricalData"])
        all_attributes = DataMetadata.list_columns_with_semantic_types(data.metadata, semantic_types=[
            "https://metadata.datadrivendiscovery.org/types/Attribute"])

        self._cat_col_index = list(set(all_attributes).intersection(categorical_attributes))
        self._cat_columns = data.columns[self._cat_col_index].tolist()

        self.logger.debug('Encoding columns: {}'.format(self._cat_columns))

        mapping = {}
        for column_name in self._cat_columns:
            col = data[column_name]
            temp = self._trim_features(col, self.hyperparams['n_limit'])
            if temp:
                mapping[temp[0]] = temp[1]
        self._mapping = mapping
        self._fitted = True
        return CallResult(None, has_finished=True)

    def produce(self, *, inputs: Input, timeout: float = None, iterations: int = None) -> CallResult[Output]:
        """
        Convert and output the input data into encoded format,
        using the trained (fitted) encoder.
        Notice that [colname]_other_ and [colname]_nan columns
        are always kept for one-hot encoded columns.
        """

        self._input_data_copy = inputs.copy()

        # Remove columns with all empty values
        self.logger.debug('Removing entirely empty columns: {}'.format(self._input_data_copy.columns[self._empty_columns]))
        self._input_data_copy = container.DataFrame.remove_columns(self._input_data_copy, self._empty_columns)

        # Return if there is nothing to encode
        if len(self._cat_columns) == 0:
            return CallResult(self._input_data_copy, True, 1)

        self.logger.debug('Encoding columns: {}'.format(self._cat_columns))

        data_encode = self._input_data_copy[list(self._mapping.keys())]

        # Get rid of false SettingWithCopyWarning
        data_encode.is_copy = None
        res = []
        for column_name in self._cat_columns:
            column_i = self._input_data_copy.metadata.get_column_index_from_column_name(column_name)
            is_str_col = self._input_data_copy.metadata.query((mbase.ALL_ELEMENTS, column_i)).get('structural_type', ()) == str
            feature = data_encode[column_name].copy()
            other_ = lambda x: 'Other' if (x and x not in self._mapping[column_name]) else x
            nan_ = lambda x: x if x else np.nan
            feature.loc[feature.notnull()] = feature[feature.notnull()].apply(other_)
            feature = feature.apply(nan_)
            if 'nan' not in self._mapping[column_name]:
                self._mapping[column_name].append('nan')
            new_column_names = ['{}_{}'.format(column_name, i) for i in self._mapping[column_name]]
            if not is_str_col:
                # TODO: Column name post-processing no longer needed once
                # https://github.com/pandas-dev/pandas/issues/20693 is resolved.
                new_column_names = self._remove_trailing_zeros(new_column_names)
            encoded = pd.get_dummies(feature, dummy_na=True, prefix=column_name)
            if not is_str_col:
                # TODO: Column name post-processing no longer needed once
                # https://github.com/pandas-dev/pandas/issues/20693 is resolved.
                encoded.columns = self._remove_trailing_zeros(encoded.columns)
            missed = [name for name in new_column_names if name not in list(encoded.columns)]
            for m in missed:
                # print('missing', m)
                encoded[m] = 0
            encoded = encoded[new_column_names]
            res.append(encoded)
            # data_encode.loc[:,column_name] = feature

        # Drop columns that will be encoded
        # data_rest = self._input_data_copy.drop(self._mapping.keys(), axis=1)
        columns_names = self._input_data_copy.columns.tolist()
        drop_indices = [columns_names.index(col) for col in self._mapping.keys()]
        drop_indices = sorted(drop_indices)

        all_categorical = False
        try:
            self._input_data_copy = container.DataFrame.remove_columns(self._input_data_copy, drop_indices)
        except ValueError:
            self.logger.warning("[warn] All the attributes are categorical!")
            all_categorical = True

        # metadata for columns that are not one hot encoded
        # self._col_index = [self._input_data_copy.columns.get_loc(c) for c in data_rest.columns]
        # data_rest.metadata = utils.select_columns_metadata(self._input_data_copy.metadata, self._col_index)

        # encode data
        # encoded = container.DataFrame(pd.get_dummies(data_encode, dummy_na=True, prefix=self._cat_columns, prefix_sep='_',
        #                                        columns=self._cat_columns))
        encoded_df = container.DataFrame(pd.concat(res, axis=1))

        # update metadata for existing columns
        for index, col_name in enumerate(encoded_df.columns):
            old_metadata = dict(encoded_df.metadata.query((mbase.ALL_ELEMENTS, index)))
            if 'name' not in old_metadata:
                old_metadata['name'] = col_name
            old_metadata["structural_type"] = int
            old_metadata["semantic_types"] = (
                'http://schema.org/Integer', 'https://metadata.datadrivendiscovery.org/types/Attribute')
            encoded_df.metadata = encoded_df.metadata.update((mbase.ALL_ELEMENTS, index), old_metadata)
        # update dimensional information
        encoded_df.metadata = encoded_df.metadata.update((), self._input_data_copy.metadata.query(()))
        columns_query = dict(self._input_data_copy.metadata.query((mbase.ALL_ELEMENTS,)))
        new_dimension_data = dict(columns_query['dimension'])
        new_dimension_data['length'] = encoded_df.shape[1]
        columns_query['dimension'] = frozendict.FrozenOrderedDict(new_dimension_data)
        encoded_df.metadata = encoded_df.metadata.update((mbase.ALL_ELEMENTS,), frozendict.FrozenOrderedDict(columns_query))
        # merge/concat both the dataframes
        if not all_categorical:
            output = container.DataFrame.horizontal_concat(self._input_data_copy, encoded_df, use_right_metadata=True)
        else:
            output = encoded_df
        return CallResult(output, True, 1)

    def get_params(self) -> EncParams:
        if not self._fitted:
            raise ValueError("Fit not performed.")
        return EncParams(
            mapping=self._mapping,
            cat_columns=self._cat_columns,
            empty_columns=self._empty_columns)

    def set_params(self, *, params: EncParams) -> None:
        self._fitted = True
        self._mapping = params['mapping']
        self._cat_columns = params['cat_columns']
        self._empty_columns = params['empty_columns']

    @classmethod
    def _get_columns_to_fit(cls, inputs: Input, hyperparams: EncHyperparameter):
        if not hyperparams['use_semantic_types']:
            return inputs, list(range(len(inputs.columns)))

        inputs_metadata = inputs.metadata

        def can_produce_column(column_index: int) -> bool:
            return cls._can_produce_column(inputs_metadata, column_index, hyperparams)

        columns_to_produce, columns_not_to_produce = utils.get_columns_to_use(
            inputs_metadata, use_columns=hyperparams['use_columns'],
            exclude_columns=hyperparams['exclude_columns'],
            can_use_column=can_produce_column)
        return inputs.iloc[:, columns_to_produce], columns_to_produce

    @classmethod
    def _can_produce_column(cls, inputs_metadata: mbase.DataMetadata, column_index: int,
                            hyperparams: EncHyperparameter) -> bool:
        column_metadata = inputs_metadata.query((mbase.ALL_ELEMENTS, column_index))

        semantic_types = column_metadata.get('semantic_types', [])
        if len(semantic_types) == 0:
            cls.logger.warning("No semantic types found in column metadata")
            return False
        if "https://metadata.datadrivendiscovery.org/types/Attribute" in semantic_types:
            return True

        return False
