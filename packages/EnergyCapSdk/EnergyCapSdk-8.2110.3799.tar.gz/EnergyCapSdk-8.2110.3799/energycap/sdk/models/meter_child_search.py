# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class MeterChildSearch(Model):
    """Class derived from MeterChildDTO - has Meter Address and Serial Number
    This class is used by the Bill Entry Account Searcher.

    :param meter_address:
    :type meter_address: ~energycap.sdk.models.AddressChild
    :param serial_number: The meter's current serial number
    :type serial_number: str
    :param previous_serial_number: The meter's previous serial number
    :type previous_serial_number: str
    :param meter_id: The meter identifier
    :type meter_id: int
    :param meter_code: The meter code
    :type meter_code: str
    :param meter_info: The meter info
    :type meter_info: str
    :param meter_type:
    :type meter_type: ~energycap.sdk.models.MeterTypeChild
    :param commodity:
    :type commodity: ~energycap.sdk.models.CommodityChild
    :param active: Indicates whether the Meter is Active
    :type active: bool
    :param is_calculated_meter: Indicates whether the Meter is a calculated
     meter
    :type is_calculated_meter: bool
    :param is_split_parent_meter: Indicates whether the Meter is a parent of a
     split
    :type is_split_parent_meter: bool
    :param is_split_child_meter: Indicates whether the Meter is a child of a
     split
    :type is_split_child_meter: bool
    """

    _attribute_map = {
        'meter_address': {'key': 'meterAddress', 'type': 'AddressChild'},
        'serial_number': {'key': 'serialNumber', 'type': 'str'},
        'previous_serial_number': {'key': 'previousSerialNumber', 'type': 'str'},
        'meter_id': {'key': 'meterId', 'type': 'int'},
        'meter_code': {'key': 'meterCode', 'type': 'str'},
        'meter_info': {'key': 'meterInfo', 'type': 'str'},
        'meter_type': {'key': 'meterType', 'type': 'MeterTypeChild'},
        'commodity': {'key': 'commodity', 'type': 'CommodityChild'},
        'active': {'key': 'active', 'type': 'bool'},
        'is_calculated_meter': {'key': 'isCalculatedMeter', 'type': 'bool'},
        'is_split_parent_meter': {'key': 'isSplitParentMeter', 'type': 'bool'},
        'is_split_child_meter': {'key': 'isSplitChildMeter', 'type': 'bool'},
    }

    def __init__(self, **kwargs):
        super(MeterChildSearch, self).__init__(**kwargs)
        self.meter_address = kwargs.get('meter_address', None)
        self.serial_number = kwargs.get('serial_number', None)
        self.previous_serial_number = kwargs.get('previous_serial_number', None)
        self.meter_id = kwargs.get('meter_id', None)
        self.meter_code = kwargs.get('meter_code', None)
        self.meter_info = kwargs.get('meter_info', None)
        self.meter_type = kwargs.get('meter_type', None)
        self.commodity = kwargs.get('commodity', None)
        self.active = kwargs.get('active', None)
        self.is_calculated_meter = kwargs.get('is_calculated_meter', None)
        self.is_split_parent_meter = kwargs.get('is_split_parent_meter', None)
        self.is_split_child_meter = kwargs.get('is_split_child_meter', None)
