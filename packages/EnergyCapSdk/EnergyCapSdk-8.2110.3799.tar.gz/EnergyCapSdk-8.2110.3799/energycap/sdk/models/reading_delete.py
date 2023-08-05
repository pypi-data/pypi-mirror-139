# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ReadingDelete(Model):
    """ReadingDelete.

    All required parameters must be populated in order to send to Azure.

    :param channel_id: Required. The identifier for the channel of the reading
     <span class='property-internal'>Required</span>
    :type channel_id: int
    :param time_begin: The begin date and time of the set of readings to be
     deleted.
     If provided, readings after but NOT including the provided begin date and
     time will be deleted.
    :type time_begin: datetime
    :param time_end: The end date and time of the set of readings to be
     deleted.
     If provided, readings up to and including the provided end date and time
     will be deleted.
    :type time_end: datetime
    """

    _validation = {
        'channel_id': {'required': True},
    }

    _attribute_map = {
        'channel_id': {'key': 'channelId', 'type': 'int'},
        'time_begin': {'key': 'timeBegin', 'type': 'iso-8601'},
        'time_end': {'key': 'timeEnd', 'type': 'iso-8601'},
    }

    def __init__(self, **kwargs):
        super(ReadingDelete, self).__init__(**kwargs)
        self.channel_id = kwargs.get('channel_id', None)
        self.time_begin = kwargs.get('time_begin', None)
        self.time_end = kwargs.get('time_end', None)
