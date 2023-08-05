# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class MeterDigestSavingsMonthlyResponseResults(Model):
    """MeterDigestSavingsMonthlyResponseResults.

    :param calendar_period: Calendar Period
    :type calendar_period: int
    :param calendar_year: Calendar Year
    :type calendar_year: int
    :param fiscal_period: Fiscal Period
    :type fiscal_period: int
    :param fiscal_year: Fiscal Year
    :type fiscal_year: int
    :param period_name: Calendar Period Name
    :type period_name: str
    :param days: The number of days in the period
    :type days: int
    :param savings_total_cost: Total Cost
    :type savings_total_cost: float
    :param batcc_native_use: BATCC (Baseline Adjusted to Current Conditions)
     Native Use
    :type batcc_native_use: float
    :param native_use: Native Use
    :type native_use: float
    :param savings_native_use: Savings Native Use = BATCCNativeUse - NativeUse
    :type savings_native_use: float
    :param batcc_common_use: BATCC (Baseline Adjusted to Current Conditions)
     Common Use
    :type batcc_common_use: float
    :param common_use: Common Use
    :type common_use: float
    :param savings_common_use: Savings Common Use = BATCCCommonUse - CommonUse
    :type savings_common_use: float
    """

    _attribute_map = {
        'calendar_period': {'key': 'calendarPeriod', 'type': 'int'},
        'calendar_year': {'key': 'calendarYear', 'type': 'int'},
        'fiscal_period': {'key': 'fiscalPeriod', 'type': 'int'},
        'fiscal_year': {'key': 'fiscalYear', 'type': 'int'},
        'period_name': {'key': 'periodName', 'type': 'str'},
        'days': {'key': 'days', 'type': 'int'},
        'savings_total_cost': {'key': 'savingsTotalCost', 'type': 'float'},
        'batcc_native_use': {'key': 'batccNativeUse', 'type': 'float'},
        'native_use': {'key': 'nativeUse', 'type': 'float'},
        'savings_native_use': {'key': 'savingsNativeUse', 'type': 'float'},
        'batcc_common_use': {'key': 'batccCommonUse', 'type': 'float'},
        'common_use': {'key': 'commonUse', 'type': 'float'},
        'savings_common_use': {'key': 'savingsCommonUse', 'type': 'float'},
    }

    def __init__(self, *, calendar_period: int=None, calendar_year: int=None, fiscal_period: int=None, fiscal_year: int=None, period_name: str=None, days: int=None, savings_total_cost: float=None, batcc_native_use: float=None, native_use: float=None, savings_native_use: float=None, batcc_common_use: float=None, common_use: float=None, savings_common_use: float=None, **kwargs) -> None:
        super(MeterDigestSavingsMonthlyResponseResults, self).__init__(**kwargs)
        self.calendar_period = calendar_period
        self.calendar_year = calendar_year
        self.fiscal_period = fiscal_period
        self.fiscal_year = fiscal_year
        self.period_name = period_name
        self.days = days
        self.savings_total_cost = savings_total_cost
        self.batcc_native_use = batcc_native_use
        self.native_use = native_use
        self.savings_native_use = savings_native_use
        self.batcc_common_use = batcc_common_use
        self.common_use = common_use
        self.savings_common_use = savings_common_use
