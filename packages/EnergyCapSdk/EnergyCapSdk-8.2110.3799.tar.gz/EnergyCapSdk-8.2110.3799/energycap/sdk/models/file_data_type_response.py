# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class FileDataTypeResponse(Model):
    """FileDataTypeResponse.

    :param file_data_type_id: The id of the file data type
    :type file_data_type_id: int
    :param file_data_type_code: The code of the file data type
    :type file_data_type_code: str
    :param file_data_type_info: The name of the file data type
    :type file_data_type_info: str
    :param supported_extensions: A list of supported extensions for this file
     data type
    :type supported_extensions: list[str]
    :param max_size_in_bytes: The maximum size, in bytes, supported for this
     file data type
    :type max_size_in_bytes: int
    """

    _attribute_map = {
        'file_data_type_id': {'key': 'fileDataTypeId', 'type': 'int'},
        'file_data_type_code': {'key': 'fileDataTypeCode', 'type': 'str'},
        'file_data_type_info': {'key': 'fileDataTypeInfo', 'type': 'str'},
        'supported_extensions': {'key': 'supportedExtensions', 'type': '[str]'},
        'max_size_in_bytes': {'key': 'maxSizeInBytes', 'type': 'int'},
    }

    def __init__(self, **kwargs):
        super(FileDataTypeResponse, self).__init__(**kwargs)
        self.file_data_type_id = kwargs.get('file_data_type_id', None)
        self.file_data_type_code = kwargs.get('file_data_type_code', None)
        self.file_data_type_info = kwargs.get('file_data_type_info', None)
        self.supported_extensions = kwargs.get('supported_extensions', None)
        self.max_size_in_bytes = kwargs.get('max_size_in_bytes', None)
