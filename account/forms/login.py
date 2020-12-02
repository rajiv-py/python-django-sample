import logging

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import login

from cheers.apps.account.models import ModelAccountUser

logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------------
# FormAccountUserLogin
# -------------------------------------------------------------------------------
class FormAccountUserLogin(forms.Form):
    """
    Form used to check user credentials, authenticate and login.
    """

    email = forms.EmailField(max_length=60, label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    # ---------------------------------------------------------------------------
    # clean
    # ---------------------------------------------------------------------------
    def clean(self):
        """
        Method to check email and password combination and authenticate a user.
        """

        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:

            try:
                user = ModelAccountUser.objects.get(email=email)
            except ModelAccountUser.DoesNotExist:
                user = None

            if user and not (user.is_staff or user.is_superuser or user.is_bar_owner):
                raise forms.ValidationError("Permission Denied.")

            if not user:
                raise forms.ValidationError("Incorrect email or password.")
            # Verify email password combination.
            self.auth_user = authenticate(email=email, password=password)

        return self.cleaned_data

    # ---------------------------------------------------------------------------
    # do_login
    # ---------------------------------------------------------------------------
    def do_login(self, request):
        """
        Method to save the user's id in the session.
        """

        login(request, self.auth_user)
