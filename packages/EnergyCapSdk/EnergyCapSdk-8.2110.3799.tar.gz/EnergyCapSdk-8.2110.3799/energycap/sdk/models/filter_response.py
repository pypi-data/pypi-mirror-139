# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class FilterResponse(Model):
    """FilterResponse.

    :param available_operator:  <span class='property-internal'>Required
     (defined)</span>
    :type available_operator: list[str]
    :param caption:  <span class='property-internal'>Required (defined)</span>
    :type caption: str
    :param query_parameter_name:  <span class='property-internal'>Required
     (defined)</span>
    :type query_parameter_name: str
    :param field_id:  <span class='property-internal'>Required
     (defined)</span>
    :type field_id: int
    :param data_field_id:  <span class='property-internal'>Required
     (defined)</span>
    :type data_field_id: int
    :param data_type:
    :type data_type: ~energycap.sdk.models.DataTypeResponse
    :param operator:  <span class='property-internal'>Required
     (defined)</span>
    :type operator: str
    :param value:  <span class='property-internal'>Required (defined)</span>
    :type value: str
    :param required:  <span class='property-internal'>Required
     (defined)</span>
    :type required: bool
    :param recommended:  <span class='property-internal'>Required
     (defined)</span>
    :type recommended: bool
    """

    _attribute_map = {
        'available_operator': {'key': 'availableOperator', 'type': '[str]'},
        'caption': {'key': 'caption', 'type': 'str'},
        'query_parameter_name': {'key': 'queryParameterName', 'type': 'str'},
        'field_id': {'key': 'fieldId', 'type': 'int'},
        'data_field_id': {'key': 'dataFieldId', 'type': 'int'},
        'data_type': {'key': 'dataType', 'type': 'DataTypeResponse'},
        'operator': {'key': 'operator', 'type': 'str'},
        'value': {'key': 'value', 'type': 'str'},
        'required': {'key': 'required', 'type': 'bool'},
        'recommended': {'key': 'recommended', 'type': 'bool'},
    }

    def __init__(self, **kwargs):
        super(FilterResponse, self).__init__(**kwargs)
        self.available_operator = kwargs.get('available_operator', None)
        self.caption = kwargs.get('caption', None)
        self.query_parameter_name = kwargs.get('query_parameter_name', None)
        self.field_id = kwargs.get('field_id', None)
        self.data_field_id = kwargs.get('data_field_id', None)
        self.data_type = kwargs.get('data_type', None)
        self.operator = kwargs.get('operator', None)
        self.value = kwargs.get('value', None)
        self.required = kwargs.get('required', None)
        self.recommended = kwargs.get('recommended', None)
