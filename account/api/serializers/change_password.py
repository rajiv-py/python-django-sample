from rest_framework import serializers


class SerializerAccountChangePassword(serializers.Serializer):
    """
    This serializer handle the change password data.
    """

    old_password = serializers.CharField()
    new_password = serializers.CharField()