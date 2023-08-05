# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ChargebackWorkflowCreate(Model):
    """ChargebackWorkflowCreate.

    All required parameters must be populated in order to send to Azure.

    :param chargeback_workflow_info: Required. Name given to the chargeback
     workflow <span class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and 64 characters</span>
    :type chargeback_workflow_info: str
    :param chargeback_workflow_steps: List of chargeback workflow steps with
     details
     Order of the steps in the list determines the steps in the workflow. <span
     class='property-internal'>Cannot be Empty</span>
    :type chargeback_workflow_steps:
     list[~energycap.sdk.models.ChargebackWorkflowStepCreate]
    """

    _validation = {
        'chargeback_workflow_info': {'required': True, 'max_length': 64, 'min_length': 0},
    }

    _attribute_map = {
        'chargeback_workflow_info': {'key': 'chargebackWorkflowInfo', 'type': 'str'},
        'chargeback_workflow_steps': {'key': 'chargebackWorkflowSteps', 'type': '[ChargebackWorkflowStepCreate]'},
    }

    def __init__(self, *, chargeback_workflow_info: str, chargeback_workflow_steps=None, **kwargs) -> None:
        super(ChargebackWorkflowCreate, self).__init__(**kwargs)
        self.chargeback_workflow_info = chargeback_workflow_info
        self.chargeback_workflow_steps = chargeback_workflow_steps
