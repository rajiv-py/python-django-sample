from rest_framework import serializers

from cheers.apps.account.models import ModelAccountUser
from cheers.apps.bar.models import ModelBarPlan
from django.utils.translation import ugettext_lazy as _


class SerializerAccountReferralCode(serializers.Serializer):

    referral_code  = serializers.CharField(max_length=200)


    def validate(self, data):
        """
        This method check the user referral code valid or not.
        """
        referral_code = data.get("referral_code", '')
        if referral_code:
            try:
                referral_user = ModelAccountUser.objects.get(referral_code=referral_code)
                if referral_user == self.context.get("request").user:
                    raise serializers.ValidationError({'referral_code': [_("you can't use your own referral code ")]})

            except ModelAccountUser.DoesNotExist:
                raise serializers.ValidationError({'referral_code': [_('This code is not valid try another')]})
        return data