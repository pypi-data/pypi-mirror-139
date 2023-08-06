from typing import Dict, List

from pyspark.sql import SparkSession
from data_quality_check.config import ConfigDataset, ConfigProfilingCustomized


class CodeCheckResult:
    field_name: str
    expected_codes: list
    null_row_count: int
    unexpected_unull_row_count: int
    unexpected_code_samples: list
    total_row_count: int

    def __init__(self, field_name: str, expected_codes: list, null_row_count: int = 0,
                 unexpected_unull_row_count: int = 0, unexpected_code_samples: list = [], total_row_count: int = 0):
        self.field_name = field_name
        self.expected_codes = expected_codes
        self.null_row_count = null_row_count
        self.unexpected_unull_row_count = unexpected_unull_row_count
        self.unexpected_code_samples = unexpected_code_samples
        self.total_row_count = total_row_count

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {
            'field_name': self.field_name,
            'expected_codes': self.expected_codes,
            'unexpected_code_samples': self.unexpected_code_samples,
            'null_row_count': self.null_row_count,
            'unexpected_unull_row_count': self.unexpected_unull_row_count,
            'total_row_count': self.total_row_count
        }


class KeyMappingCheckResult:
    field_name: str
    target_table: str
    target_column: str
    outstanding_value_samples: list
    outstanding_row_count: int
    null_and_empty_row_count: int
    total_row_count: int

    def __init__(self, field_name: str, target_table: str, target_column: str,
                 outstanding_value_samples: list = [], outstanding_row_count: int = 0,
                 null_and_empty_row_count: int = 0,
                 total_row_count: int = 0):
        self.field_name = field_name
        self.target_table = target_table
        self.target_column = target_column
        self.outstanding_value_samples = outstanding_value_samples
        self.outstanding_row_count = outstanding_row_count
        self.null_and_empty_row_count = null_and_empty_row_count
        self.total_row_count = total_row_count

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {
            'field_name': self.field_name,
            'target_table': self.target_table,
            'target_column': self.target_column,
            'outstanding_value_samples': self.outstanding_value_samples,
            'outstanding_row_count': self.outstanding_row_count,
            'null_and_empty_row_count': self.null_and_empty_row_count,
            'total_row_count': self.total_row_count
        }


class CustomizedProfilerResult:
    code_check_result: List[CodeCheckResult] = []
    key_mapping_check_result: List[KeyMappingCheckResult] = []

    def __init__(self, code_check_result: Dict = None, key_mapping_check_result: Dict = None):
        if code_check_result is not None:
            self.code_check_result = code_check_result

        if key_mapping_check_result is not None:
            self.key_mapping_check_result = key_mapping_check_result

    def has_code_check_result(self):
        return len(self.code_check_result) > 0

    def has_key_mapping_check_result(self):
        return len(self.key_mapping_check_result) > 0

    def to_dict(self):
        result = {}
        if self.has_code_check_result():
            result['code_check'] = []
            for cc in self.code_check_result:
                result['code_check'].append(cc.to_dict())

        # Key Mapping Check
        if self.has_key_mapping_check_result():
            result['key_mapping_check'] = []
            for kmc in self.key_mapping_check_result:
                result['key_mapping_check'].append(kmc.to_dict())
        return result


class CustomizedProfiler:
    dataset_config: ConfigDataset
    profiling_config: ConfigProfilingCustomized
    spark: SparkSession

    def __init__(self, spark, dataset_config: ConfigDataset,
                 customized_profiling_config: ConfigProfilingCustomized = ConfigProfilingCustomized()):
        self.spark = spark
        self.dataset_config = dataset_config
        self.profiling_config = customized_profiling_config

    def code_check(self, table_name: str, field_name: str, expected_codes: list = []):
        expected_codes.sort()
        expected_codes_raw_str = str(expected_codes)
        expected_codes_str = str(expected_codes_raw_str).replace('[', '').replace(']', '')

        sql = f'SELECT 1 FROM {table_name}  WHERE `{field_name}` IS NULL '
        null_row_count = self.spark.sql(sql).count()

        sql = f'SELECT 1 FROM {table_name} ' \
              f' WHERE `{field_name}` NOT IN ({expected_codes_str}) AND `{field_name}` IS NOT NULL'
        unexpected_unull_row_count = self.spark.sql(sql).count()

        sql = f'SELECT 1 FROM {table_name} '
        total_row_count = self.spark.sql(sql).count()

        sql = f'SELECT COLLECT_SET(DISTINCT(`{field_name}`)) AS result_set, 1 AS one FROM {table_name} ' \
              f' WHERE `{field_name}` NOT IN ({expected_codes_str}) GROUP BY one LIMIT 50'
        sql_result = self.spark.sql(sql).collect()
        if len(sql_result) > 0:
            unexpected_code_samples = sql_result[0]['result_set']
        else:
            unexpected_code_samples = []
        return CodeCheckResult(field_name, expected_codes=expected_codes, null_row_count=null_row_count,
                               unexpected_unull_row_count=unexpected_unull_row_count,
                               unexpected_code_samples=unexpected_code_samples, total_row_count=total_row_count)

    def key_mapping_check(self, table_name, field_name, target_table_name, target_field_name):
        sql = f'SELECT COLLECT_SET(result) AS result_set, 1 AS one from ' \
              f' (SELECT DISTINCT(aa.{field_name}) as result FROM {table_name} aa ' \
              f' LEFT ANTI JOIN {target_table_name} bb ' \
              f' ON (aa.{field_name} = bb.{target_field_name}) ' \
              f' WHERE TRIM(aa.{field_name})!=\'\' AND aa.{field_name} IS NOT NULL order by result asc LIMIT 100) ' \
              f' GROUP BY one'
        sql_result = self.spark.sql(sql).collect()
        if len(sql_result) > 0:
            outstanding_value_samples = sql_result[0]['result_set']
        else:
            outstanding_value_samples = []

        sql = f' SELECT 1 FROM {table_name} aa ' \
              f' LEFT ANTI JOIN {target_table_name} bb ' \
              f' ON (aa.{field_name} = bb.{target_field_name}) ' \
              f' WHERE TRIM(aa.{field_name})!=\'\' AND aa.{field_name} IS NOT NULL'
        outstanding_row_count = self.spark.sql(sql).count()

        sql = f'SELECT 1 FROM {table_name} '
        total_row_count = self.spark.sql(sql).count()

        sql = f' SELECT 1 FROM {table_name} WHERE TRIM({field_name})=\'\' OR {field_name} IS NULL'
        null_and_empty_row_count = self.spark.sql(sql).count()

        return KeyMappingCheckResult(field_name=field_name, target_table=target_table_name,
                                     target_column=target_field_name,
                                     outstanding_value_samples=outstanding_value_samples,
                                     outstanding_row_count=outstanding_row_count,
                                     null_and_empty_row_count=null_and_empty_row_count, total_row_count=total_row_count)

    def run(self, return_type='dict'):
        table_name = self.dataset_config.name
        customized_profiler_result = CustomizedProfilerResult()

        # Code Check
        code_check_list = self.profiling_config.code_check
        if code_check_list is not None and len(code_check_list) > 0:
            for cc in code_check_list:
                cc_result = self.code_check(table_name=table_name, field_name=cc.column, expected_codes=cc.codes)
                customized_profiler_result.code_check_result.append(cc_result)

        # Key Mapping Check
        key_mapping_check_list = self.profiling_config.key_mapping_check
        if key_mapping_check_list is not None and len(key_mapping_check_list) > 0:
            for kmc in key_mapping_check_list:
                kmc_result = self.key_mapping_check(table_name=table_name, field_name=kmc.column,
                                                    target_table_name=kmc.target_table,
                                                    target_field_name=kmc.target_column)
                customized_profiler_result.key_mapping_check_result.append(kmc_result)

        if return_type == 'dict':
            return customized_profiler_result.to_dict()
        else:
            return customized_profiler_result
