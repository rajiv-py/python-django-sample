from dateutil.relativedelta import relativedelta
from django import forms

from cheers.apps.account.models import ModelAccountUser
from cheers.apps.bar.models import ModelBarPlan


class FormPayment(forms.Form):
    stripeToken = forms.CharField(max_length=255)
    referral_code  = forms.CharField(max_length=255, initial="i8vCFY")


    # def clean(self):
    #
    #     referral_code = self.cleaned_data.get("referral_code", '')
    #     plan = ModelBarPlan.objects.get(duration=1)
    #     if referral_code:
    #         try:
    #             referral_user = ModelAccountUser.objects.get(referral_code=referral_code)
    #             if not referral_user.referral_status:
    #                 try:
    #                     print(referral_user)
    #                     subscription = referral_user.subscription
    #                     print(subscription.expiration, "subscription")
    #                     print(subscription.expiration + relativedelta(months=1))
    #                     print("here")
    #                 except AttributeError:
    #                     print("pass here")
    #                     pass
    #                 # plan.subscribe(referral_user)
    #         except ModelAccountUser.DoesNotExist:
    #             raise forms.ValidationError({'referral_code': 'This code is not valid try another'})
    #
    #     return self.cleaned_data

