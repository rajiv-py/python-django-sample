"""
                        ACCOUNT URL'S
"""


from django.urls.conf import path
from django.urls.conf import re_path

from cheers.apps.account.views.change_password import ViewAccountChangePassword
from cheers.apps.account.views.dashboard import ViewAccountDashboard
from cheers.apps.account.views.forgot_password import ViewAccountForgotPassword
from cheers.apps.account.views.login import ViewAccountUserLogin
from cheers.apps.account.views.password_verification import ViewAccountForgotPasswordVerification
from cheers.apps.account.views.payment_test import ViewPaymentTest
from cheers.apps.account.views.logout import ViewAccountLogout
from cheers.apps.account.views.profile import ViewAccountProfile
from cheers.apps.account.views.wizard.add_bar import ViewAccountWizardAddBar

urlpatterns = [

    path('verification/', ViewAccountForgotPasswordVerification.as_view(),
         name="password-verification"),

    path('change-password/', ViewAccountChangePassword.as_view(),
         name="change-password"),

    path('login/', ViewAccountUserLogin.as_view(),
         name="login"),

    path('logout/', ViewAccountLogout.as_view(),name="logout"),

    path('dashboard/', ViewAccountDashboard.as_view(),
         name="dashboard"),

    path('profile/', ViewAccountProfile.as_view(),
         name="profile"),

    path('forgot-password/', ViewAccountForgotPassword.as_view(),
         name="forgot-password"),

    path('payment/', ViewPaymentTest.as_view(),
         name="payment"),

    path('wizard/add-bar/', ViewAccountWizardAddBar.as_view(),
         name="wizard-add-bar"),




]
