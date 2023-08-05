# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ObservationMethodChild(Model):
    """ObservationMethodChild.

    :param observation_method_id: Observation method identifier
    :type observation_method_id: int
    :param observation_method_code: Observation method code
    :type observation_method_code: str
    :param observation_method_info: Observation method name: Automatic,
     Manual, Estimated, Simulated, Accrual, or Adjustment
    :type observation_method_info: str
    """

    _attribute_map = {
        'observation_method_id': {'key': 'observationMethodId', 'type': 'int'},
        'observation_method_code': {'key': 'observationMethodCode', 'type': 'str'},
        'observation_method_info': {'key': 'observationMethodInfo', 'type': 'str'},
    }

    def __init__(self, *, observation_method_id: int=None, observation_method_code: str=None, observation_method_info: str=None, **kwargs) -> None:
        super(ObservationMethodChild, self).__init__(**kwargs)
        self.observation_method_id = observation_method_id
        self.observation_method_code = observation_method_code
        self.observation_method_info = observation_method_info
