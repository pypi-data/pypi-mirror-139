# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ReportDistributionLogDetailsResponse(Model):
    """ReportDistributionLogDetailsResponse.

    :param email_settings:
    :type email_settings:
     ~energycap.sdk.models.ReportDistributionLogEmailSettings
    :param report_settings:
    :type report_settings:
     ~energycap.sdk.models.ReportDistributionLogReportSettings
    :param errors: Detailed errors that may have occurred during report
     distribution run
    :type errors: str
    """

    _attribute_map = {
        'email_settings': {'key': 'emailSettings', 'type': 'ReportDistributionLogEmailSettings'},
        'report_settings': {'key': 'reportSettings', 'type': 'ReportDistributionLogReportSettings'},
        'errors': {'key': 'errors', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(ReportDistributionLogDetailsResponse, self).__init__(**kwargs)
        self.email_settings = kwargs.get('email_settings', None)
        self.report_settings = kwargs.get('report_settings', None)
        self.errors = kwargs.get('errors', None)
