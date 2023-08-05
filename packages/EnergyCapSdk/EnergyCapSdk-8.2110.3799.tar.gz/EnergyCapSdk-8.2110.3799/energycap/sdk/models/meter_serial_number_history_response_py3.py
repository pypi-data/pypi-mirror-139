# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class MeterSerialNumberHistoryResponse(Model):
    """MeterSerialNumberHistoryResponse.

    :param meter_id: Meter identifier <span class='property-internal'>Required
     (defined)</span>
    :type meter_id: int
    :param serial_number: Serial number of the meter <span
     class='property-internal'>Required (defined)</span>
    :type serial_number: str
    :param serial_number_history:
    :type serial_number_history:
     ~energycap.sdk.models.MeterSerialNumberHistoryChild
    """

    _attribute_map = {
        'meter_id': {'key': 'meterId', 'type': 'int'},
        'serial_number': {'key': 'serialNumber', 'type': 'str'},
        'serial_number_history': {'key': 'serialNumberHistory', 'type': 'MeterSerialNumberHistoryChild'},
    }

    def __init__(self, *, meter_id: int=None, serial_number: str=None, serial_number_history=None, **kwargs) -> None:
        super(MeterSerialNumberHistoryResponse, self).__init__(**kwargs)
        self.meter_id = meter_id
        self.serial_number = serial_number
        self.serial_number_history = serial_number_history
