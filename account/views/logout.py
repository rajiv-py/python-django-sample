from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse
from django.views.generic.base import RedirectView


# -------------------------------------------------------------------------------
# ViewAccountUserLogout
# -------------------------------------------------------------------------------
class ViewAccountLogout(LoginRequiredMixin, RedirectView):
    """
    View to handle logout process.
    """

    permanent = False

    # ---------------------------------------------------------------------------
    # get_redirect_url
    # ---------------------------------------------------------------------------
    def get_redirect_url(self, *args, **kwargs):
        """
        Method to logout user and redirect it to the login screen.
        """

        if self.request.user.is_authenticated:
            logout(self.request)

        messages.info(self.request, 'Come back soon!')

        return reverse('account:login')