# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class CalculatedBillUseResponse(Model):
    """Definition of how a calculated bill will get its use.

    :param readings_from_channel:
    :type readings_from_channel:
     ~energycap.sdk.models.ChannelChildWithObservationType
    :param fixed_amount:
    :type fixed_amount: ~energycap.sdk.models.FixedAmountResponse
    :param copy_use_from_meter:
    :type copy_use_from_meter: ~energycap.sdk.models.CopyFromMeterResponse
    :param use_calculation:
    :type use_calculation: ~energycap.sdk.models.CalculationResponse
    """

    _attribute_map = {
        'readings_from_channel': {'key': 'readingsFromChannel', 'type': 'ChannelChildWithObservationType'},
        'fixed_amount': {'key': 'fixedAmount', 'type': 'FixedAmountResponse'},
        'copy_use_from_meter': {'key': 'copyUseFromMeter', 'type': 'CopyFromMeterResponse'},
        'use_calculation': {'key': 'useCalculation', 'type': 'CalculationResponse'},
    }

    def __init__(self, **kwargs):
        super(CalculatedBillUseResponse, self).__init__(**kwargs)
        self.readings_from_channel = kwargs.get('readings_from_channel', None)
        self.fixed_amount = kwargs.get('fixed_amount', None)
        self.copy_use_from_meter = kwargs.get('copy_use_from_meter', None)
        self.use_calculation = kwargs.get('use_calculation', None)
