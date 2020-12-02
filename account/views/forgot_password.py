from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView

# -------------------------------------------------------------------------------
# ViewAccountForgotPassword
# -------------------------------------------------------------------------------
from cheers.apps.account.forms.forgot_password import FormAccountForgotPassword
from cheers.apps.account.models import ModelAccountVerification


class ViewAccountForgotPassword(FormView):
    """
    View used for user forgot password functionality.
    """

    form_class = FormAccountForgotPassword
    template_name = "account/forgot-password.html"
    success_url = reverse_lazy('account:login')


    # ---------------------------------------------------------------------------
    # form_valid
    # ---------------------------------------------------------------------------
    def form_valid(self, form):
        """
        Sends the reset password key to the user.
        """

        ModelAccountVerification.objects.send_verification_email(form.user,
                                                                 verification_type=
                                                                 ModelAccountVerification.VERIFICATION_TYPES[1][0])

        messages.info(self.request, "Email sent successfully to the {0}".format(form.user.email))

        return HttpResponseRedirect(self.success_url)
