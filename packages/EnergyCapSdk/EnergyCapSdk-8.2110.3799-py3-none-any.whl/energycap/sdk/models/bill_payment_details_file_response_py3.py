# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class BillPaymentDetailsFileResponse(Model):
    """BillPaymentDetailsFileResponse.

    :param success: Number of successful bill payment detail updates <span
     class='property-internal'>Required (defined)</span>
    :type success: int
    :param failure: Number of unsuccessful bill payment detail updates <span
     class='property-internal'>Required (defined)</span>
    :type failure: int
    :param kickout_stream: Base64 encoded File content of unsuccessful bill
     payment detail updates with reasons for failure <span
     class='property-internal'>Required (defined)</span>
    :type kickout_stream: str
    """

    _attribute_map = {
        'success': {'key': 'success', 'type': 'int'},
        'failure': {'key': 'failure', 'type': 'int'},
        'kickout_stream': {'key': 'kickoutStream', 'type': 'str'},
    }

    def __init__(self, *, success: int=None, failure: int=None, kickout_stream: str=None, **kwargs) -> None:
        super(BillPaymentDetailsFileResponse, self).__init__(**kwargs)
        self.success = success
        self.failure = failure
        self.kickout_stream = kickout_stream
