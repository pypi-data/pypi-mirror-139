from django.core.validators import RegexValidator

from expressmoney.api import *

__all__ = ('UserFileAPI',)
SERVICE_NAME = 'storage'


class UserFileContract(Contract):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z_]*$', 'Only alphanumeric characters are allowed.')

    id = serializers.IntegerField(min_value=1)
    name = serializers.CharField(max_length=64, validators=(alphanumeric,))
    file = serializers.URLField()
    public_url = serializers.URLField(allow_null=True)


class UserFileAPI(API):
    _contract = UserFileContract
    _service_name = SERVICE_NAME
    _app = 'storage'
    _point = 'user_file'


class UploadFileAPI(API):
    _contract = None
    _service_name = SERVICE_NAME
    _app = 'storage'
    _point = 'upload_file'
