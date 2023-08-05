# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class RouteRequest(Model):
    """RouteRequest.

    All required parameters must be populated in order to send to Azure.

    :param route_info: Required. The route info <span
     class='property-internal'>Must be between 0 and 32 characters</span> <span
     class='property-internal'>Required</span>
    :type route_info: str
    :param route_code: The route code
     This property has been deprecated. Route code will be generated from the
     value in route info <span class='property-internal'>Must be between 0 and
     16 characters</span>
    :type route_code: str
    :param meter_ids: Required. The list of IDs for meters to be assigned to
     the route. The order in which the meter IDs appear will determine their
     order on the route.
     NOTE: if the same meter ID is passed in multiple times, the first
     occurrence of the meter ID will be used to determine the order on the
     route <span class='property-internal'>Required</span>
    :type meter_ids: list[int]
    """

    _validation = {
        'route_info': {'required': True, 'max_length': 32, 'min_length': 0},
        'route_code': {'max_length': 16, 'min_length': 0},
        'meter_ids': {'required': True},
    }

    _attribute_map = {
        'route_info': {'key': 'routeInfo', 'type': 'str'},
        'route_code': {'key': 'routeCode', 'type': 'str'},
        'meter_ids': {'key': 'meterIds', 'type': '[int]'},
    }

    def __init__(self, *, route_info: str, meter_ids, route_code: str=None, **kwargs) -> None:
        super(RouteRequest, self).__init__(**kwargs)
        self.route_info = route_info
        self.route_code = route_code
        self.meter_ids = meter_ids
