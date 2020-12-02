from rest_framework import serializers
from cheers.apps.account.models import ModelAccountUser


# -------------------------------------------------------------------------------
# SerializerAccountLogin
# -------------------------------------------------------------------------------
class SerializerAccountLogin(serializers.Serializer):
    """
    Validates all data that is sent while trying to login manually.
    """

    email = serializers.CharField()
    password = serializers.CharField()
    device_token = serializers.CharField()
    device_type = serializers.ChoiceField(choices=ModelAccountUser.DEVICE_TYPES)
