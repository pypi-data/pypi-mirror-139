# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class CalculatedBillCostRequest(Model):
    """Defines how use is calculated for a calculated bill distribution.

    :param use_current_meters_rate_schedule: Apply the meter's current rate
     when calculating bill cost
     "true" is the only valid value for this property <span
     class='property-internal'>One of True </span> <span
     class='property-internal'>Required (defined)</span>
    :type use_current_meters_rate_schedule: bool
    :param fixed_unit_cost:
    :type fixed_unit_cost: ~energycap.sdk.models.FixedUnitCostRequest
    :param unit_cost_meter_id: MeterId from where to get the unit cost <span
     class='property-internal'>Required (defined)</span>
    :type unit_cost_meter_id: int
    :param fixed_amount: Use a fixed amount for bill cost <span
     class='property-info'>Max scale of 2</span> <span
     class='property-info'>NULL Valid</span> <span
     class='property-internal'>Required (defined)</span>
    :type fixed_amount: float
    :param copy_cost_from_meter:
    :type copy_cost_from_meter: ~energycap.sdk.models.CopyMeterRequest
    :param cost_calculation:
    :type cost_calculation: ~energycap.sdk.models.CalculationRequest
    """

    _attribute_map = {
        'use_current_meters_rate_schedule': {'key': 'useCurrentMetersRateSchedule', 'type': 'bool'},
        'fixed_unit_cost': {'key': 'fixedUnitCost', 'type': 'FixedUnitCostRequest'},
        'unit_cost_meter_id': {'key': 'unitCostMeterId', 'type': 'int'},
        'fixed_amount': {'key': 'fixedAmount', 'type': 'float'},
        'copy_cost_from_meter': {'key': 'copyCostFromMeter', 'type': 'CopyMeterRequest'},
        'cost_calculation': {'key': 'costCalculation', 'type': 'CalculationRequest'},
    }

    def __init__(self, **kwargs):
        super(CalculatedBillCostRequest, self).__init__(**kwargs)
        self.use_current_meters_rate_schedule = kwargs.get('use_current_meters_rate_schedule', None)
        self.fixed_unit_cost = kwargs.get('fixed_unit_cost', None)
        self.unit_cost_meter_id = kwargs.get('unit_cost_meter_id', None)
        self.fixed_amount = kwargs.get('fixed_amount', None)
        self.copy_cost_from_meter = kwargs.get('copy_cost_from_meter', None)
        self.cost_calculation = kwargs.get('cost_calculation', None)
