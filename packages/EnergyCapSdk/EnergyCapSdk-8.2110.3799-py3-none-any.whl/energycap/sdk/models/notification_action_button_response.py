# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class NotificationActionButtonResponse(Model):
    """NotificationActionButtonResponse.

    :param url: Url the action will link to
    :type url: str
    :param label: Label the action will display
    :type label: str
    :param open_in_new_window: Should clicking the action link open a new
     window
    :type open_in_new_window: bool
    """

    _attribute_map = {
        'url': {'key': 'url', 'type': 'str'},
        'label': {'key': 'label', 'type': 'str'},
        'open_in_new_window': {'key': 'openInNewWindow', 'type': 'bool'},
    }

    def __init__(self, **kwargs):
        super(NotificationActionButtonResponse, self).__init__(**kwargs)
        self.url = kwargs.get('url', None)
        self.label = kwargs.get('label', None)
        self.open_in_new_window = kwargs.get('open_in_new_window', None)
