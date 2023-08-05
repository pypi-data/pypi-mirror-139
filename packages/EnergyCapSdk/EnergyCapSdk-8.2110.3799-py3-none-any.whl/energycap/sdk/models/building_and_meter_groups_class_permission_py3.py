# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class BuildingAndMeterGroupsClassPermission(Model):
    """BuildingAndMeterGroupsClassPermission.

    :param create:
    :type create: bool
    :param edit:
    :type edit: bool
    :param delete:
    :type delete: bool
    """

    _attribute_map = {
        'create': {'key': 'create', 'type': 'bool'},
        'edit': {'key': 'edit', 'type': 'bool'},
        'delete': {'key': 'delete', 'type': 'bool'},
    }

    def __init__(self, *, create: bool=None, edit: bool=None, delete: bool=None, **kwargs) -> None:
        super(BuildingAndMeterGroupsClassPermission, self).__init__(**kwargs)
        self.create = create
        self.edit = edit
        self.delete = delete
