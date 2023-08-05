# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class WorkflowSettingsResponse(Model):
    """WorkflowSettingsResponse.

    :param batch:
    :type batch: ~energycap.sdk.models.BatchWorkflowSettings
    :param approval:
    :type approval: ~energycap.sdk.models.ApprovalWorkflowChild
    :param ap_export:
    :type ap_export: ~energycap.sdk.models.ExportWorkflowChild
    :param gl_export:
    :type gl_export: ~energycap.sdk.models.ExportWorkflowChild
    :param chargeback:
    :type chargeback: ~energycap.sdk.models.ChargebackWorkflowSettings
    """

    _attribute_map = {
        'batch': {'key': 'batch', 'type': 'BatchWorkflowSettings'},
        'approval': {'key': 'approval', 'type': 'ApprovalWorkflowChild'},
        'ap_export': {'key': 'apExport', 'type': 'ExportWorkflowChild'},
        'gl_export': {'key': 'glExport', 'type': 'ExportWorkflowChild'},
        'chargeback': {'key': 'chargeback', 'type': 'ChargebackWorkflowSettings'},
    }

    def __init__(self, *, batch=None, approval=None, ap_export=None, gl_export=None, chargeback=None, **kwargs) -> None:
        super(WorkflowSettingsResponse, self).__init__(**kwargs)
        self.batch = batch
        self.approval = approval
        self.ap_export = ap_export
        self.gl_export = gl_export
        self.chargeback = chargeback
