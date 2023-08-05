# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class BillMeterBodyLineCreate(Model):
    """BillMeterBodyLineCreate.

    All required parameters must be populated in order to send to Azure.

    :param observation_type_id: Required. The bodyline's observation type
     <span class='property-internal'>Required</span>
    :type observation_type_id: int
    :param value_unit_id: The bodyline's unit of measure
    :type value_unit_id: int
    :param value: The line item's value
    :type value: float
    :param cost_unit_id: The bodyline's cost unit of measure for this
    :type cost_unit_id: int
    :param cost: The cost attributed to the line item
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
        'observation_type_id': {'key': 'observationTypeId', 'type': 'int'},
        'value_unit_id': {'key': 'valueUnitId', 'type': 'int'},
        'value': {'key': 'value', 'type': 'float'},
        'cost_unit_id': {'key': 'costUnitId', 'type': 'int'},
        'cost': {'key': 'cost', 'type': 'float'},
        'caption': {'key': 'caption', 'type': 'str'},
    }

    def __init__(self, *, observation_type_id: int, caption: str, value_unit_id: int=None, value: float=None, cost_unit_id: int=None, cost: float=None, **kwargs) -> None:
        super(BillMeterBodyLineCreate, self).__init__(**kwargs)
        self.observation_type_id = observation_type_id
        self.value_unit_id = value_unit_id
        self.value = value
        self.cost_unit_id = cost_unit_id
        self.cost = cost
        self.caption = caption
