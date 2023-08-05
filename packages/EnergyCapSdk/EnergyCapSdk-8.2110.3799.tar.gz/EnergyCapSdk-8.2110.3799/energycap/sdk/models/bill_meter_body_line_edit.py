# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class BillMeterBodyLineEdit(Model):
    """BillMeterBodyLineEdit.

    All required parameters must be populated in order to send to Azure.

    :param body_line_id: The bodyline's id for an existing bodyline <span
     class='property-internal'>Required (defined)</span>
    :type body_line_id: int
    :param observation_type_id: Required. The bodyline's observation type
     <span class='property-internal'>Required</span>
    :type observation_type_id: int
    :param value_unit_id: The bodyline's unit of measure <span
     class='property-internal'>Required (defined)</span>
    :type value_unit_id: int
    :param value: The line item's value <span
     class='property-internal'>Required (defined)</span>
    :type value: float
    :param cost_unit_id: The bodyline's cost unit of measure for this <span
     class='property-internal'>Required (defined)</span>
    :type cost_unit_id: int
    :param cost: The cost attributed to the line item <span
     class='property-internal'>Required (defined)</span>
    :type cost: float
    :param caption: Required. The caption <span
     class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and 32 characters</span>
    :type caption: str
    """

    _validation = {
        'observation_type_id': {'required': True},
        'caption': {'required': True, 'max_length': 32, 'min_length': 0},
    }

    _attribute_map = {
        'body_line_id': {'key': 'bodyLineId', 'type': 'int'},
        'observation_type_id': {'key': 'observationTypeId', 'type': 'int'},
        'value_unit_id': {'key': 'valueUnitId', 'type': 'int'},
        'value': {'key': 'value', 'type': 'float'},
        'cost_unit_id': {'key': 'costUnitId', 'type': 'int'},
        'cost': {'key': 'cost', 'type': 'float'},
        'caption': {'key': 'caption', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(BillMeterBodyLineEdit, self).__init__(**kwargs)
        self.body_line_id = kwargs.get('body_line_id', None)
        self.observation_type_id = kwargs.get('observation_type_id', None)
        self.value_unit_id = kwargs.get('value_unit_id', None)
        self.value = kwargs.get('value', None)
        self.cost_unit_id = kwargs.get('cost_unit_id', None)
        self.cost = kwargs.get('cost', None)
        self.caption = kwargs.get('caption', None)
