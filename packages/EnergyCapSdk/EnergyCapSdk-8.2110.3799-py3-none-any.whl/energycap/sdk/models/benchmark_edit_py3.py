# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class BenchmarkEdit(Model):
    """BenchmarkEdit.

    All required parameters must be populated in order to send to Azure.

    :param benchmark_category_id: Required. benchmark category Id <span
     class='property-internal'>Required</span>
    :type benchmark_category_id: int
    :param benchmark_info: Required. benchmark name <span
     class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and 255 characters</span>
    :type benchmark_info: str
    """

    _validation = {
        'benchmark_category_id': {'required': True},
        'benchmark_info': {'required': True, 'max_length': 255, 'min_length': 0},
    }

    _attribute_map = {
        'benchmark_category_id': {'key': 'benchmarkCategoryId', 'type': 'int'},
        'benchmark_info': {'key': 'benchmarkInfo', 'type': 'str'},
    }

    def __init__(self, *, benchmark_category_id: int, benchmark_info: str, **kwargs) -> None:
        super(BenchmarkEdit, self).__init__(**kwargs)
        self.benchmark_category_id = benchmark_category_id
        self.benchmark_info = benchmark_info
