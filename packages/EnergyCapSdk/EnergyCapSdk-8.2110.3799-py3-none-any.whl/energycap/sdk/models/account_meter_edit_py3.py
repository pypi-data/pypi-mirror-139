# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class AccountMeterEdit(Model):
    """AccountMeterEdit.

    :param begin_date: The beginning date and time for this account meter
     relationship <span class='property-internal'>Must be between 12/31/1899
     and 1/1/3000</span> <span class='property-internal'>Required
     (defined)</span>
    :type begin_date: datetime
    :param end_date: The ending date and time for this account meter
     relationship <span class='property-internal'>Must be between 12/31/1899
     and 1/1/3000</span> <span class='property-internal'>Required
     (defined)</span>
    :type end_date: datetime
    :param general_ledger_id: The identifier for the general ledger assigned
     to this account meter <span class='property-internal'>Required
     (defined)</span>
    :type general_ledger_id: int
    :param vendor_type_id: The identifier for the vendor type. Vendors may
     assume different types on different account meters <span
     class='property-internal'>Required (defined)</span>
    :type vendor_type_id: int
    """

    _attribute_map = {
        'begin_date': {'key': 'beginDate', 'type': 'iso-8601'},
        'end_date': {'key': 'endDate', 'type': 'iso-8601'},
        'general_ledger_id': {'key': 'generalLedgerId', 'type': 'int'},
        'vendor_type_id': {'key': 'vendorTypeId', 'type': 'int'},
    }

    def __init__(self, *, begin_date=None, end_date=None, general_ledger_id: int=None, vendor_type_id: int=None, **kwargs) -> None:
        super(AccountMeterEdit, self).__init__(**kwargs)
        self.begin_date = begin_date
        self.end_date = end_date
        self.general_ledger_id = general_ledger_id
        self.vendor_type_id = vendor_type_id
