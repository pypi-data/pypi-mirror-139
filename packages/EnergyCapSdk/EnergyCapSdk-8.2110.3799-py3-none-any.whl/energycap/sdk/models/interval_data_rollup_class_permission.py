# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class IntervalDataRollupClassPermission(Model):
    """IntervalDataRollupClassPermission.

    :param run:
    :type run: bool
    """

    _attribute_map = {
        'run': {'key': 'run', 'type': 'bool'},
    }

    def __init__(self, **kwargs):
        super(IntervalDataRollupClassPermission, self).__init__(**kwargs)
        self.run = kwargs.get('run', None)
