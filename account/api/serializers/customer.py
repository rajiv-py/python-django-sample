# from django.contrib.auth.hashers import make_password
# from rest_framework import serializers
#
# from cheers.apps.account.api.serializers.user import SerializerAccountUserUpdate
# from cheers.apps.account.models import ModelAccountCustomer
#
#
# # -------------------------------------------------------------------------------
# # SerializerAccountCustomer
# # -------------------------------------------------------------------------------
# class SerializerAccountCustomer(serializers.ModelSerializer):
#     """
#     Validates and serializes the data of an account user.
#     """
#     number = serializers.SerializerMethodField()
#     country_code = serializers.SerializerMethodField()
#     # ---------------------------------------------------------------------------
#     # Meta
#     # ---------------------------------------------------------------------------
#     class Meta:
#         model = ModelAccountCustomer
#         fields = ('id', 'email', 'password', 'name', "device_token",
#                   'avatar', 'address', 'phone_number', "number", "country_code")
#
#
#     def create(self, validated_data):
#         validated_data['password'] = make_password(validated_data.get('password'))
#         return super(SerializerAccountCustomer, self).create(validated_data)
#
#     def get_number(self, obj):
#         if obj.phone_number:
#             return obj.phone_number.national_number
#
#     def get_country_code(self, obj):
#         if obj.phone_number:
#             return obj.phone_number.country_code
#
# class SerializerAccountCustomerUpdate(SerializerAccountUserUpdate):
#     """
#     """
#     date_of_birth = serializers.DateField(required=False)
#
#     # This is just for a caution. Although this serializer is not meant to be
#     # used for POST requests
#     def create(self, validated_data):
#         return super(serializers.ModelSerializer, self).create(validated_data)

