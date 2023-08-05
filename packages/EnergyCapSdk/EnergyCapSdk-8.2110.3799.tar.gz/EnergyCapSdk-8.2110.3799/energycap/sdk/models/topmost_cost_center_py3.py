# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class TopmostCostCenter(Model):
    """TopmostCostCenter.

    :param is_multi_topmost_cost_center: User's topmost combines multiple cost
     centers
    :type is_multi_topmost_cost_center: bool
    :param multi_topmost_cost_centers:
    :type multi_topmost_cost_centers:
     list[~energycap.sdk.models.CostCenterChild]
    :param cost_center_id: The cost center identifier
    :type cost_center_id: int
    :param cost_center_code: The cost center code
    :type cost_center_code: str
    :param cost_center_info: The cost center info
    :type cost_center_info: str
    """

    _attribute_map = {
        'is_multi_topmost_cost_center': {'key': 'isMultiTopmostCostCenter', 'type': 'bool'},
        'multi_topmost_cost_centers': {'key': 'multiTopmostCostCenters', 'type': '[CostCenterChild]'},
        'cost_center_id': {'key': 'costCenterId', 'type': 'int'},
        'cost_center_code': {'key': 'costCenterCode', 'type': 'str'},
        'cost_center_info': {'key': 'costCenterInfo', 'type': 'str'},
    }

    def __init__(self, *, is_multi_topmost_cost_center: bool=None, multi_topmost_cost_centers=None, cost_center_id: int=None, cost_center_code: str=None, cost_center_info: str=None, **kwargs) -> None:
        super(TopmostCostCenter, self).__init__(**kwargs)
        self.is_multi_topmost_cost_center = is_multi_topmost_cost_center
        self.multi_topmost_cost_centers = multi_topmost_cost_centers
        self.cost_center_id = cost_center_id
        self.cost_center_code = cost_center_code
        self.cost_center_info = cost_center_info
