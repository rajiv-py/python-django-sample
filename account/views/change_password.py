from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.views.generic.edit import FormView
from cheers.apps.account.forms.change_password import FormAccountChangePassword

# -------------------------------------------------------------------------------
# ViewAccountChangePassword
# -------------------------------------------------------------------------------
class ViewAccountChangePassword(FormView):
    """
    View used to change a user's account password.
    """

    form_class = FormAccountChangePassword
    template_name = "account/change-password.html"
    success_url = reverse_lazy("account:change-password")

    # ---------------------------------------------------------------------------
    # form_valid
    # ---------------------------------------------------------------------------
    def form_valid(self, form):
        """
        Saves the changed password for user account.
        """

        # Checks user in the session
        user = self.request.user

        # Updates the user's password
        user.set_password(form.cleaned_data.get('password'))
        user.save()

        messages.info(self.request, 'Password has been changed successfully')

        return HttpResponseRedirect(self.success_url)

    # ---------------------------------------------------------------------------
    # get_form_kwargs
    # ---------------------------------------------------------------------------
    def get_form_kwargs(self):
        kwargs = FormView.get_form_kwargs(self)
        kwargs['request'] = self.request

        return kwargs