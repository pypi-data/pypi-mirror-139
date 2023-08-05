# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class BillSplitDetailsRequest(Model):
    """Defines details for available types of bill split distributions. Only one
    of the properties may be populated.

    :param fixed_percentage_split: Populate if setting up a fixed percentage
     split.
     You cannot split to the same account and meter combination multiple times
     within a single version.
     The destination account cannot be the same as the master account <span
     class='property-internal'>Cannot be Empty</span> <span
     class='property-internal'>NULL Valid</span> <span
     class='property-internal'>Required (defined)</span>
    :type fixed_percentage_split: list[~energycap.sdk.models.FixedPercentage]
    :param floor_area_split: Populate if setting up a dynamic percentage split
     based on the building floor area with weighting factor applied.
     You cannot split the same account and meter multiple times within a single
     version.
     You cannot split to the same account and meter combination multiple times
     within a single version.
     The destination account cannot be the same as the master account <span
     class='property-internal'>Cannot be Empty</span> <span
     class='property-internal'>NULL Valid</span> <span
     class='property-internal'>Required (defined)</span>
    :type floor_area_split: list[~energycap.sdk.models.FloorAreaSplit]
    :param dynamic_percentage_split:
    :type dynamic_percentage_split:
     ~energycap.sdk.models.DynamicPercentageBillSplit
    """

    _attribute_map = {
        'fixed_percentage_split': {'key': 'fixedPercentageSplit', 'type': '[FixedPercentage]'},
        'floor_area_split': {'key': 'floorAreaSplit', 'type': '[FloorAreaSplit]'},
        'dynamic_percentage_split': {'key': 'dynamicPercentageSplit', 'type': 'DynamicPercentageBillSplit'},
    }

    def __init__(self, **kwargs):
        super(BillSplitDetailsRequest, self).__init__(**kwargs)
        self.fixed_percentage_split = kwargs.get('fixed_percentage_split', None)
        self.floor_area_split = kwargs.get('floor_area_split', None)
        self.dynamic_percentage_split = kwargs.get('dynamic_percentage_split', None)
