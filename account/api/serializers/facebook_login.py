from rest_framework import serializers
from cheers.apps.account.models import ModelAccountUser


# -------------------------------------------------------------------------------
# SerializerFacebookLogin
# -------------------------------------------------------------------------------
class SerializerFacebookLogin(serializers.Serializer):
    """
    Validates access token that is sent while trying to login through facebook.
    """

    access_token = serializers.CharField(max_length=500)
