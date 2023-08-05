# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class GuidResponse(Model):
    """GuidResponse.

    :param task_gu_id: A guid that identifies the current task
    :type task_gu_id: str
    """

    _attribute_map = {
        'task_gu_id': {'key': 'taskGUId', 'type': 'str'},
    }

    def __init__(self, *, task_gu_id: str=None, **kwargs) -> None:
        super(GuidResponse, self).__init__(**kwargs)
        self.task_gu_id = task_gu_id
