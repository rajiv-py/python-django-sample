from django.db import models
from urllib.parse import urlencode

from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.core.mail import send_mail
from cheers.apps.account.managers.verification import ManagerAccountVerification
from cheers.apps.account.models import ModelAccountUser
from cheers.settings import BASE_URL, DEFAULT_FROM_EMAIL
from django.core.mail import EmailMultiAlternatives

class ModelAccountVerification(models.Model):
    """
    This model is used for storing verification information for a user.
    """

    VERIFICATION_TYPES = ((0, 'registration'), (1, 'password'))

    user = models.OneToOneField(ModelAccountUser, on_delete=models.CASCADE,
                                related_name="verification",
                                help_text="A user of the account which is due"
                                          "account verification.")

    token = models.CharField(max_length=100,
                             help_text="A unique uuid 4 based token sent in"
                                       "the email as a link.")

    type = models.IntegerField(choices=VERIFICATION_TYPES,
                               default=VERIFICATION_TYPES[1][0],
                               help_text="Decides what type of request needs "
                                         "to be verified.")

    expiration = models.DateTimeField(help_text="Number of days for which the"
                                                "verification token is valid.")

    objects = ManagerAccountVerification()

    # ---------------------------------------------------------------------------
    # Meta
    # ---------------------------------------------------------------------------
    class Meta:
        db_table = "account_verification"
        verbose_name = "Verification"
        verbose_name_plural = "Verifications"

    # ---------------------------------------------------------------------------
    # __str__
    # ---------------------------------------------------------------------------
    def __str__(self):
        """
        Returns string representation of the user's email.
        """

        return self.user.email

    # ---------------------------------------------------------------------------
    # verification_url
    # ---------------------------------------------------------------------------
    @property
    def verification_url(self):
        """
        A shortcut property to generate a verification link.
        """

        params = urlencode({'token': self.token})
        return "%s%s?%s" % (BASE_URL, reverse('account:email-verification'),
                            params)

    # ---------------------------------------------------------------------------
    # verification_url
    # ---------------------------------------------------------------------------
    @property
    def verification_url_for_password(self):
        """
        A shortcut property to generate a verification link for password.
        """

        params = urlencode({'token': self.token, "password": True})
        return "%s%s?%s" % (BASE_URL,
                            reverse('account:password-verification'), params)

    # ---------------------------------------------------------------------------
    # has_expired
    # ---------------------------------------------------------------------------
    @property
    def has_expired(self):
        """
        Returns a boolean value based on whether the verification has expired.
        """

        return False if timezone.now() <= self.expiration else True

    # ---------------------------------------------------------------------------
    # send_verification_email
    # ---------------------------------------------------------------------------
    def send_verification_email(self):
        """
        Sends the user a verification email.
        """

        subject = "Forgot Password"
        context_data = {"name": self.user.get_name,
                        "verification_link": self.verification_url_for_password}

        html_template_path = "emails/user-verification-email.html"
        text_template_path = 'emails/user-verification-email.txt'

        html_content = render_to_string(html_template_path, context_data)

        msg = EmailMultiAlternatives(subject, text_template_path, DEFAULT_FROM_EMAIL, [self.user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()




