from django.contrib.auth.hashers import make_password
from drf_extra_fields.fields import Base64ImageField
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from cheers.apps.account.models import ModelAccountUser, ModelAccountReference

# -------------------------------------------------------------------------------
# SerializerAccountUser
# -------------------------------------------------------------------------------
from cheers.apps.base.utility.misc import randomStringDigits


class SerializerAccountUser(serializers.ModelSerializer):
    """
    Validates and serializes the data of an account user.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    date_of_birth = serializers.DateField(required=True)
    number = serializers.SerializerMethodField()
    country_code = serializers.SerializerMethodField()
    code = serializers.CharField(required=False)
    avatar = Base64ImageField(required=False)
    coupon_history = serializers.SerializerMethodField()

    # ---------------------------------------------------------------------------
    # Meta
    # ---------------------------------------------------------------------------
    class Meta:
        model = ModelAccountUser
        fields = ('id', 'email', 'password', 'first_name', 'surname', 'city', 'language',  "device_type",
                  "device_token", "date_of_birth",
                  'avatar', 'address', 'phone_number', "number", "country_code", 'referral_code', "code",
                  'coupon_history', "stripe_customer")

    def create(self, validated_data):

        validated_data['password'] = make_password(validated_data.get('password'))
        validated_data['referral_code'] = randomStringDigits()
        code = validated_data.pop('code', '')

        # save referee and referrer information
        if code:
            try:
                referrer_from = ModelAccountUser.objects.get(referral_code=code)
                print(referrer_from)
            except ModelAccountUser.DoesNotExist:
                raise serializers.ValidationError({'code': [_('This code is not valid')]})
            instance = super(SerializerAccountUser, self).create(validated_data)
            ModelAccountReference.objects.create(referrer_from=referrer_from, code=code, referrer_to=instance)
        else:
            instance = super(SerializerAccountUser, self).create(validated_data)
        return instance

    def get_number(self, obj):
        if obj.phone_number:
            return obj.phone_number.national_number

    def get_country_code(self, obj):
        if obj.phone_number:
            return obj.phone_number.country_code

    def get_coupon_history(self, obj):

        coupons = []
        coupon_dict = {}
        for user in obj.users.all():
            print(user.coupon.code)
            coupon_dict[user.coupon.code] = user.coupon.description
        coupons.append(coupon_dict)
        return coupons



class SerializerAccountUserUpdate(SerializerAccountUser):
    """
    """
    
    phone_number = PhoneNumberField()

    # This is just for a caution. Although this serializer is not meant to be
    # used for POST requests
    def create(self, validated_data):
        return super(serializers.ModelSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get("password"):
            validated_data['password'] = make_password(validated_data.get('password'))
        return super(SerializerAccountUserUpdate, self).update(instance, validated_data)

