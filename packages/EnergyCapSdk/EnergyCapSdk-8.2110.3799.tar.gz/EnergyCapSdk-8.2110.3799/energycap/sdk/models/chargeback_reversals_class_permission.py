# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ChargebackReversalsClassPermission(Model):
    """ChargebackReversalsClassPermission.

    :param manage:
    :type manage: bool
    """

    _attribute_map = {
        'manage': {'key': 'manage', 'type': 'bool'},
    }

    def __init__(self, **kwargs):
        super(ChargebackReversalsClassPermission, self).__init__(**kwargs)
        self.manage = kwargs.get('manage', None)
