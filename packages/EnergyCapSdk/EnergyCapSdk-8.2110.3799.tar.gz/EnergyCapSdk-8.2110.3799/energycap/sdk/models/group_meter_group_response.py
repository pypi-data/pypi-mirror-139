# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class GroupMeterGroupResponse(Model):
    """GroupMeterGroupResponse.

    :param meter_group_id: The meter group identifier
    :type meter_group_id: int
    :param meter_group_code: The meter group code
    :type meter_group_code: str
    :param meter_group_info: The meter group info
    :type meter_group_info: str
    :param auto_group: Indicates if this meter group is an autogroup
    :type auto_group: bool
    :param member_count: The number of meters in this group
    :type member_count: int
    :param member_count_with_topmost: The number of meters within the
     currently authenticated user's topmost
    :type member_count_with_topmost: int
    :param meter_group_category:
    :type meter_group_category: ~energycap.sdk.models.MeterGroupCategoryChild
    :param limit_members_by_topmost: Indicates if the meter group has been set
     limit the list of members by the user's topmost
    :type limit_members_by_topmost: bool
    :param user_defined_auto_group: Indicates if this meter group is an user
     defined auto group
    :type user_defined_auto_group: bool
    :param user_defined_auto_group_filters: The filters applied to determine
     the members of a user defined auto group
    :type user_defined_auto_group_filters:
     list[~energycap.sdk.models.FilterResponse]
    :param last_updated: The last time a member was inserted, updated, or
     deleted from the group
    :type last_updated: datetime
    :param member_commodity_code: The commodity code for the meters in this
     group -
     if all meters belong to the same commodity the commodity code will be used
     here
     if meters belong to different commodities, value will be "MULTIPLE"
     if this group has no meters, value will be ""
    :type member_commodity_code: str
    """

    _attribute_map = {
        'meter_group_id': {'key': 'meterGroupId', 'type': 'int'},
        'meter_group_code': {'key': 'meterGroupCode', 'type': 'str'},
        'meter_group_info': {'key': 'meterGroupInfo', 'type': 'str'},
        'auto_group': {'key': 'autoGroup', 'type': 'bool'},
        'member_count': {'key': 'memberCount', 'type': 'int'},
        'member_count_with_topmost': {'key': 'memberCountWithTopmost', 'type': 'int'},
        'meter_group_category': {'key': 'meterGroupCategory', 'type': 'MeterGroupCategoryChild'},
        'limit_members_by_topmost': {'key': 'limitMembersByTopmost', 'type': 'bool'},
        'user_defined_auto_group': {'key': 'userDefinedAutoGroup', 'type': 'bool'},
        'user_defined_auto_group_filters': {'key': 'userDefinedAutoGroupFilters', 'type': '[FilterResponse]'},
        'last_updated': {'key': 'lastUpdated', 'type': 'iso-8601'},
        'member_commodity_code': {'key': 'memberCommodityCode', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(GroupMeterGroupResponse, self).__init__(**kwargs)
        self.meter_group_id = kwargs.get('meter_group_id', None)
        self.meter_group_code = kwargs.get('meter_group_code', None)
        self.meter_group_info = kwargs.get('meter_group_info', None)
        self.auto_group = kwargs.get('auto_group', None)
        self.member_count = kwargs.get('member_count', None)
        self.member_count_with_topmost = kwargs.get('member_count_with_topmost', None)
        self.meter_group_category = kwargs.get('meter_group_category', None)
        self.limit_members_by_topmost = kwargs.get('limit_members_by_topmost', None)
        self.user_defined_auto_group = kwargs.get('user_defined_auto_group', None)
        self.user_defined_auto_group_filters = kwargs.get('user_defined_auto_group_filters', None)
        self.last_updated = kwargs.get('last_updated', None)
        self.member_commodity_code = kwargs.get('member_commodity_code', None)
