from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseRedirect, Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.base import RedirectView
from cheers.apps.account.models import ModelAccountVerification


# -------------------------------------------------------------------------------
# ViewAccountForgotPasswordVerification
# -------------------------------------------------------------------------------
class ViewAccountForgotPasswordVerification(RedirectView):
    """
    View redirects the user to the change password page once the user clicks on
    link that they get in their email if it is valid.
    """

    permanent = False

    # ---------------------------------------------------------------------------
    # get
    # ---------------------------------------------------------------------------
    def get(self, request, *args, **kwargs):
        """
        This method is used to get the token and the token's user, if the token
        hasn't expired yet then the user is auto logged in to their account,
        and redirected to the change password url to change their password.
        """

        token = self.request.GET.get('token')

        try:
            verification = \
                ModelAccountVerification.objects.get(token=token,
                                                     type=ModelAccountVerification.VERIFICATION_TYPES[1][0])
        except ObjectDoesNotExist:
            raise Http404
            return redirect(reverse('account:expire-verification-message'))

        if verification.has_expired:
            raise Http404
            return redirect(reverse('account:expire-verification-message'))

        user = ModelAccountVerification.objects.verify_password(token)
        user.auto_login(self.request)
        messages.info(self.request, "Change Password")

        return HttpResponseRedirect(reverse("account:change-password"))