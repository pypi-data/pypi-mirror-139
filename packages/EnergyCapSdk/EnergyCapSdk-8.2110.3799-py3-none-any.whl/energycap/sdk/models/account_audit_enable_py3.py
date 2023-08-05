# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class AccountAuditEnable(Model):
    """AccountAuditEnable.

    :param account_ids: List of AccountIds to try and update <span
     class='property-internal'>Cannot be Empty</span> <span
     class='property-internal'>Required (defined)</span>
    :type account_ids: list[int]
    :param audit_enabled: True to allow the accounts' bills to be audited
     False to exclude the accounts' bills from being audited <span
     class='property-internal'>Required (defined)</span>
    :type audit_enabled: bool
    """

    _attribute_map = {
        'account_ids': {'key': 'accountIds', 'type': '[int]'},
        'audit_enabled': {'key': 'auditEnabled', 'type': 'bool'},
    }

    def __init__(self, *, account_ids=None, audit_enabled: bool=None, **kwargs) -> None:
        super(AccountAuditEnable, self).__init__(**kwargs)
        self.account_ids = account_ids
        self.audit_enabled = audit_enabled
