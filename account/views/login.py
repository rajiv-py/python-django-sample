import logging

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.views.generic.edit import FormView

from cheers.apps.account.forms.login import FormAccountUserLogin

logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------------
# ViewAccountUserLogin
# -------------------------------------------------------------------------------
class ViewAccountUserLogin(SuccessMessageMixin, FormView):
    """
    View used to login a user.
    """

    form_class = FormAccountUserLogin
    template_name = 'account/login.html'


    # ---------------------------------------------------------------------------
    # get
    # ---------------------------------------------------------------------------
    def get(self, request, *args, **kwargs):
        """
        If the user not logged in then redirect to login page with message.
        """
        response = FormView.get(self, request, *args, **kwargs)

        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())

        return response

    # ---------------------------------------------------------------------------
    # get_success_url
    # ---------------------------------------------------------------------------
    def get_success_url(self):
        """
        method to redirect user to the requested url if found else redirect
        to dashboard.
        """
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        if self.request.user.bars.all().exists():
            return reverse_lazy('account:dashboard')
        else:
            return reverse_lazy("bar:add-bar")


    # ---------------------------------------------------------------------------
    # form_valid
    # ---------------------------------------------------------------------------
    def form_valid(self, form):
        """
        Method to log in user and thereafter redirect to the dashboard.
        """

        # Redirect un-verified user's to resend verification page.
        if form.auth_user:
            form.do_login(self.request)
            messages.info(self.request, 'Welcome back %s' % self.request.user)

        return SuccessMessageMixin.form_valid(self, form)

