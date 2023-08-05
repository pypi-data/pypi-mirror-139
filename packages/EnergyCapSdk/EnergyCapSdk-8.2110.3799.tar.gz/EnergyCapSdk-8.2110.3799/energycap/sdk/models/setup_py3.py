# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class Setup(Model):
    """Setup.

    :param type: Type of importer. Possible values include: 'UNKNOWNTYPE',
     'CREATE_AccountsAndMeters', 'CREATE_BuildingsAndOrganizations',
     'CREATE_CostAvoidanceOtherSavings',
     'CREATE_CostAvoidanceSpecialAdjustments', 'CREATE_CostCenters',
     'CREATE_Customers', 'CREATE_ChargebackDistributionsVersions',
     'CREATE_RateSchedules', 'CREATE_Vendors', 'CREATE_Channels',
     'UPDATE_CostCenters', 'UPDATE_BuildingsAndOrganizations',
     'UPDATE_AccountingCalendar', 'UPDATE_Accounts',
     'UPDATE_CustomFieldsAccount', 'UPDATE_CostAvoidanceOtherSavings',
     'UPDATE_CostAvoidanceSpecialAdjustments', 'UPDATE_Customers',
     'CREATE_GLCodesAndSubcodes', 'UPDATE_GLCodesAndSubcodes', 'UPDATE_Meters',
     'UPDATE_CustomFieldsMeter', 'UPDATE_CustomFieldsPlace', 'UPDATE_Users',
     'UPDATE_Vendors', 'UPDATE_CustomFieldsVendor', 'CREATE_Users',
     'UPDATE_Channels', 'UPDATE_BillCalculations', 'CREATE_BillCalculations',
     'UPDATE_BillSplits', 'CREATE_BillSplits', 'UPDATE_MeterGroups',
     'UPDATE_BuildingGroups', 'CONVERT_BillSplits', 'CONVERT_BillCalculations',
     'CREATE_Readings', 'UPDATE_Readings', 'CREATE_MonthlyReadings',
     'CREATE_PlaceBenchmarks', 'UPDATE_PlaceBenchmarks', 'CREATE_UserGroups',
     'UPDATE_UserGroups', 'UPDATE_UserGroupMembers',
     'UPDATE_PlaceEnergyStarLink', 'CREATE_BudgetWorksheet'
    :type type: str or ~energycap.sdk.models.enum
    :param sheet_type: Type of sheet that was imported
    :type sheet_type: str
    :param action: Action that was performed - create, update, convert
    :type action: str
    :param success: Count of rows that succeeded
    :type success: int
    :param failure: Count of rows that failed
    :type failure: int
    :param skip: Count of rows that were skipped
    :type skip: int
    :param kickout: A stream that represents the kickout file
    :type kickout: str
    :param start: Time at which the import started
    :type start: datetime
    :param finish: Time at which the import finished
    :type finish: datetime
    :param task_id: Unique identifier for this import
    :type task_id: int
    """

    _attribute_map = {
        'type': {'key': 'type', 'type': 'str'},
        'sheet_type': {'key': 'sheetType', 'type': 'str'},
        'action': {'key': 'action', 'type': 'str'},
        'success': {'key': 'success', 'type': 'int'},
        'failure': {'key': 'failure', 'type': 'int'},
        'skip': {'key': 'skip', 'type': 'int'},
        'kickout': {'key': 'kickout', 'type': 'str'},
        'start': {'key': 'start', 'type': 'iso-8601'},
        'finish': {'key': 'finish', 'type': 'iso-8601'},
        'task_id': {'key': 'taskId', 'type': 'int'},
    }

    def __init__(self, *, type=None, sheet_type: str=None, action: str=None, success: int=None, failure: int=None, skip: int=None, kickout: str=None, start=None, finish=None, task_id: int=None, **kwargs) -> None:
        super(Setup, self).__init__(**kwargs)
        self.type = type
        self.sheet_type = sheet_type
        self.action = action
        self.success = success
        self.failure = failure
        self.skip = skip
        self.kickout = kickout
        self.start = start
        self.finish = finish
        self.task_id = task_id
