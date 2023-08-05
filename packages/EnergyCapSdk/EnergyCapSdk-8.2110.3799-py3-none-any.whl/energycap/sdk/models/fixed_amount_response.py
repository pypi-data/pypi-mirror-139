# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class FixedAmountResponse(Model):
    """Fixed amount per unit to apply during bill calculation.

    :param amount: Fixed amount
    :type amount: float
    :param unit:
    :type unit: ~energycap.sdk.models.UnitChild
    """

    _attribute_map = {
        'amount': {'key': 'amount', 'type': 'float'},
        'unit': {'key': 'unit', 'type': 'UnitChild'},
    }

    def __init__(self, **kwargs):
        super(FixedAmountResponse, self).__init__(**kwargs)
        self.amount = kwargs.get('amount', None)
        self.unit = kwargs.get('unit', None)
