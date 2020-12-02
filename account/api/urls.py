from django.conf.urls import include
from django.conf.urls import url
from rest_framework import routers

from cheers.apps.account.api.views.change_password import ViewAPIAccountChangePassword
from cheers.apps.account.api.views.check_referral_code import ViewAPIAccountCheckReferralCode
from cheers.apps.account.api.views.check_user_drink_status import ViewAPIAccountUserDrinkStatus
from cheers.apps.account.api.views.facebook_login import ViewAPIFacebookLogin
from cheers.apps.account.api.views.forgot_password import ViewAPIAccountForgotPassword
from cheers.apps.account.api.views.login import ViewAPIAccountLogin
from cheers.apps.account.api.views.customer import ViewAPIAccountManageUser
from cheers.apps.account.api.views.reference import ViewAPIAccountReference
from cheers.apps.bar.api.views.order import ViewAPIBarOrder

router = routers.DefaultRouter()

# User's has signup (POST), detail (GET), update (PATCH, PUT) api's
router.register('users', ViewAPIAccountManageUser, base_name='users')


urlpatterns = [
               
    url(r'^', include(router.urls)),

    url(r'^login/$',
            ViewAPIAccountLogin.as_view(), name='login'),\

    url(r'^facebook-login/$',
            ViewAPIFacebookLogin.as_view(), name='facebook-login'),

    url(r'^references/$',
            ViewAPIAccountReference.as_view(), name='references'),

    url(r'^change-password/$',
        ViewAPIAccountChangePassword.as_view(), name='change-password'),

    url(r'^forgot-password/$',
            ViewAPIAccountForgotPassword.as_view(), name='forgot-password'),

    url(r'^user-drink-status/$',
            ViewAPIAccountUserDrinkStatus.as_view(), name='user-drink-status'),

    url(r'^validate-referral_code/$',
            ViewAPIAccountCheckReferralCode.as_view(), name='validate-referral_code'),


    #
    # url(r'^profile/$',
    #     ViewAPIAccountProfile.as_view(), name='profile'),
    #
    # url(r'^verification/$',
    #     ViewAccountVerification.as_view(), name='verification'),
    #
    # url(r'^resend-verification/$', #This is we are doing via knockout and REST api's
    #     ViewAPIAccountResendVerification.as_view(), name='resend-verification'),
    #
    # url(r'^business-profile/$', #This is we are doing via knockout and REST api's
    #     ViewAPIBusinessManageProfile.as_view(), name='business-profile'),
    #
               
]
