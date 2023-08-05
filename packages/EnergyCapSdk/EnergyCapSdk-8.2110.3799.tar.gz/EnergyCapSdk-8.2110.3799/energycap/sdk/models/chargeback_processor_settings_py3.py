# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ChargebackProcessorSettings(Model):
    """The settings used to run the chargeback processor.

    All required parameters must be populated in order to send to Azure.

    :param filters: Optional Filters. These will aid in identifying the
     distributions that should be processed
     TODO:List applicable filters
    :type filters: list[~energycap.sdk.models.QuickFilter]
    :param billing_period: Required. Billing Period to be processed <span
     class='property-internal'>Required</span>
    :type billing_period: int
    :param start_date_for_bill: Optional Start Date for Bill being generated.
     Only used for Calculate Bill and that too when use is not from sub-meter
     reading
     The bills generated will inherit bill headers (accounting period, invoice
     number, control code, etc ) from the batch <span
     class='property-internal'>Must be between 12/31/1899 and 1/1/3000</span>
    :type start_date_for_bill: datetime
    :param end_date_for_bill: Optional End Date for Bill being generated. Only
     used for Calculate Bill and that too when use is not from sub-meter
     reading
     The bills generated will inherit bill headers (accounting period, invoice
     number, control code, etc ) from the batch <span
     class='property-internal'>Must be between 12/31/1899 and 1/1/3000</span>
    :type end_date_for_bill: datetime
    :param note: Optional note/comment <span class='property-internal'>Must be
     between 0 and 255 characters</span>
    :type note: str
    :param batch_settings:
    :type batch_settings: ~energycap.sdk.models.BatchCreate
    """

    _validation = {
        'billing_period': {'required': True},
        'note': {'max_length': 255, 'min_length': 0},
    }

    _attribute_map = {
        'filters': {'key': 'filters', 'type': '[QuickFilter]'},
        'billing_period': {'key': 'billingPeriod', 'type': 'int'},
        'start_date_for_bill': {'key': 'startDateForBill', 'type': 'iso-8601'},
        'end_date_for_bill': {'key': 'endDateForBill', 'type': 'iso-8601'},
        'note': {'key': 'note', 'type': 'str'},
        'batch_settings': {'key': 'batchSettings', 'type': 'BatchCreate'},
    }

    def __init__(self, *, billing_period: int, filters=None, start_date_for_bill=None, end_date_for_bill=None, note: str=None, batch_settings=None, **kwargs) -> None:
        super(ChargebackProcessorSettings, self).__init__(**kwargs)
        self.filters = filters
        self.billing_period = billing_period
        self.start_date_for_bill = start_date_for_bill
        self.end_date_for_bill = end_date_for_bill
        self.note = note
        self.batch_settings = batch_settings
