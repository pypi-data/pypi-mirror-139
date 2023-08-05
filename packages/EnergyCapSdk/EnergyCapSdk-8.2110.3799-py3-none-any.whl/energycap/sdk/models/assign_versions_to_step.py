# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class AssignVersionsToStep(Model):
    """AssignVersionsToStep.

    :param calculate_bill_version_ids: List of calculated bill or bill split
     version IDs to assign to a chargeback workflow step <span
     class='property-internal'>Required (defined)</span>
    :type calculate_bill_version_ids: list[int]
    """

    _attribute_map = {
        'calculate_bill_version_ids': {'key': 'calculateBillVersionIds', 'type': '[int]'},
    }

    def __init__(self, **kwargs):
        super(AssignVersionsToStep, self).__init__(**kwargs)
        self.calculate_bill_version_ids = kwargs.get('calculate_bill_version_ids', None)
