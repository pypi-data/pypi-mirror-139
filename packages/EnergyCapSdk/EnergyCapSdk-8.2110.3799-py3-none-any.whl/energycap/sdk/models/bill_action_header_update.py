# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class BillActionHeaderUpdate(Model):
    """BillActionHeaderUpdate.

    All required parameters must be populated in order to send to Azure.

    :param bill_ids: Required. Bill IDs whose headers are going to be updated
     <span class='property-internal'>Cannot be Empty</span> <span
     class='property-internal'>Required</span>
    :type bill_ids: list[int]
    :param bill_header: Required.
    :type bill_header: ~energycap.sdk.models.BillHeaderUpdate
    """

    _validation = {
        'bill_ids': {'required': True},
        'bill_header': {'required': True},
    }

    _attribute_map = {
        'bill_ids': {'key': 'billIds', 'type': '[int]'},
        'bill_header': {'key': 'billHeader', 'type': 'BillHeaderUpdate'},
    }

    def __init__(self, **kwargs):
        super(BillActionHeaderUpdate, self).__init__(**kwargs)
        self.bill_ids = kwargs.get('bill_ids', None)
        self.bill_header = kwargs.get('bill_header', None)
