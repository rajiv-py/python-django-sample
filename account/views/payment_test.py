from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
import stripe
from cheers.apps.account.forms.payment import FormPayment
from cheers.apps.account.models import ModelAccountUser
from cheers.apps.bar.models import ModelBarPlan, ModelBarSubscription
from cheers.settings import STRIPE_SECRET_KEY


class ViewPaymentTest(FormView):
    form_class = FormPayment
    template_name = "account/payment_test.html"
    success_url = reverse_lazy("account:payment")
    # charge_dict = dict()


    def form_valid(self, form):
        form_data = form.cleaned_data
        print(form_data)
        stripe.api_key = STRIPE_SECRET_KEY

        token = form_data['stripeToken']
        user = ModelAccountUser.objects.get(email="bsar@cheers.com").stripe_customer['id']
        plan = ModelBarPlan.objects.first()

        # charge = stripe.PaymentIntent.create(
        #     amount=round(plan.price) * 100,
        #     currency=plan.currency,
        #     setup_future_usage='off_session',
        # )

        # customer = stripe.Customer.create(
        #     email=user.email,
        #     source='tok_mastercard',
        # )
        #
        # source = stripe.Customer.create_source(
        #           user,
        #           source=token
        #         )
        # print(source)
        #
        # stripe.Customer.list_sources(
        #     user,
        #     limit=3,
        #     object='card'
        # )

        charge = stripe.Charge.create(
            amount=round(plan.price)*100,
            currency=plan.currency,
            customer=user,
            source='card_1FIBdxLLJS3MdsEAtxCMK2TM'
        )

        # charge = stripe.Charge.create(
        #     amount=round(plan.price)*100,
        #     currency=plan.currency,
        #     description='Example charge',
        #     source=token,
        # )
        # print(charge)
        print(charge)
        # expiration = add_months(month=plan.duration)
        # subscription_data = {"user": user,
        #                      "plan": plan,
        #                      "expiration": expiration,
        #                      "transaction_details": charge
        #                      }

        # if charge.get("status") == "succeeded":
        #     plan.subscribe(user, transaction_details=charge)
        # self.charge_dict["client_secret"] = charge.get("client_secret")
        return HttpResponseRedirect(self.success_url)

    # def get_context_data(self, **kwargs):
    #     context = super(ViewPaymentTest, self).get_context_data()
    #     try:
    #         context['client_secret'] = self.charge_dict
    #         print("hererer")
    #     except:
    #         pass
    #     return context



