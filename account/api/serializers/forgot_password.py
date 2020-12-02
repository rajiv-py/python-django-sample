from rest_framework import serializers


class SerializerAccounForgotPassword(serializers.Serializer):
    """
    Validates all data that is sent while trying to reset a users password.
    """

    email = serializers.EmailField()