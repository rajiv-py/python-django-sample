import logging
from datetime import datetime
from uuid import uuid4
import os
from django.contrib.auth import login
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from cheers.apps.account.managers.user import ManagerAccountUser
from cheers.apps.base.models import ModelBaseCountry
from cheers.apps.base.models.base import ModelAbstractBase
from cheers.apps.base.utility.misc import get_user_media_upload_path
from cheers.settings import STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------------
# get_profile_picture_name
# -------------------------------------------------------------------------------
def get_profile_picture_name(instance, filename):
    try:
        file_extension = os.path.splitext(filename)[1]
    except ValueError:
        file_extension = '.unknown'

    return '{0}_avatar{1}'.format(str(uuid4()), file_extension)


# -----------------------------------------------------------------------------
# get_upload_path
# -----------------------------------------------------------------------------
def get_upload_path(instance, filename):
    """
    Get dynamic path to upload user profile picture.
    File will be uploaded to
        MEDIA_ROOT/user_<email>/<uuid4>_avatar.<extension>
    """

    upload_path = get_user_media_upload_path(instance, uploadtype="image")

    return '{0}/{1}'.format(upload_path,
                            get_profile_picture_name(instance, filename))


# ------------------------------------------------------------------------------
# ModelAccountUser
# ------------------------------------------------------------------------------
class ModelAccountUser(AbstractBaseUser, ModelAbstractBase, PermissionsMixin):
    """
    Stores authentication information about a user of the system.
    """

    DEVICE_TYPES = (('android', 'Android'), ('ios', 'Ios'))
    LANGUAGES = (('fr', 'French'), ('en', 'English'))
    email = models.EmailField(unique=True, help_text="Email of the user.")

    first_name = models.CharField(max_length=200, help_text="User's first name.",
                            null=True, blank=True)

    surname = models.CharField(max_length=200, help_text="User's surname.",
                                  null=True, blank=True)

    city = models.ForeignKey(ModelBaseCountry, null=True, blank=True,  related_name="user", on_delete=models.CASCADE)
    language = models.CharField(choices=LANGUAGES,
                                default=LANGUAGES[0][0],
                                max_length=60,
                                null=True, blank=True,
                                help_text="Language of the user.")

    phone_number = PhoneNumberField(blank=True)

    address = models.TextField(blank=True, null=True)

    avatar = models.ImageField(upload_to=get_upload_path,
                               max_length=500,
                               null=True, blank=True,
                               help_text="User's avatar.")

    facebook_id = models.CharField(max_length=25, unique=True, null=True, blank=True)

    stripe_customer = JSONField(default=dict, null=True, blank=True)

    date_of_birth = models.DateField(null=True, blank=True)

    device_token = models.CharField(max_length=200, null=True, blank=True,
                                    help_text="User Device Token",
                                    )
    device_type = models.CharField(choices=DEVICE_TYPES,
                                   max_length=60,
                                   null=True, blank=True,
                                   help_text="Device type of the user.")

    referral_code = models.CharField(max_length=20, null=True, blank=True,
                                     help_text="Referral code of the user.")

    is_active = \
    models.BooleanField(default=True,
                        help_text="Toggles active status for a user.")


    is_staff = models.BooleanField(default=False,
                                   help_text="Designates the user as "
                                             "a staff member.")

    is_superuser = models.BooleanField(default=False,
                                       help_text="Designates the user as"
                                                 " a super user.")
    is_bar_owner = models.BooleanField(default=False,
                                       help_text="Designates the user as"
                                                 " a bar owner.")

    referral_status = models.BooleanField(default=False,
                                       help_text="check the status of referral code used or not")


    objects = ManagerAccountUser()
    USERNAME_FIELD = 'email'

    # -------------------------------------------------------------------------
    # Meta
    # -------------------------------------------------------------------------
    class Meta:

        db_table = "account_user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    # ---------------------------------------------------------------------------
    # __str__
    # ---------------------------------------------------------------------------
    def __str__(self):
        """
        Returns the string representation of the user object.
        """

        return self.email


    def save(self, *args, **kwargs):
        """
        Overrides default save to make sure:
        """

        # create a strip customer when one is not available
        if not self.stripe_customer:
            self.create_stripe_customer()

        super(ModelAccountUser, self).save(*args, **kwargs)


    def create_stripe_customer(self, source_token=None):
        import stripe

        if not self.stripe_customer:
            stripe.api_key = STRIPE_SECRET_KEY

            try:
                params = {'email': self.get_username()}

                if source_token:
                    token_id = source_token['id']
                    params['source'] = token_id

                self.stripe_customer = stripe.Customer.create(**params)
                self.save()
            except Exception as e:
                logger.error('Error creating stripe customer: %s', e.__str__())
                raise ObjectDoesNotExist('Error creating stripe customer: %s', e.__str__())

    # ---------------------------------------------------------------------------
    # auto_login
    # ---------------------------------------------------------------------------
    def auto_login(self, request):
        """
        A shortcut to auto login in a user, without using the user's password.
        """

        self.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, self)

    @property
    def is_today_order_allowed(self):
        return self.orders.filter(created__date=datetime.today().date()).exists()

    @property
    def get_name(self):
        return self.first_name if self.first_name else self.email

    @property
    def subscription(self):
        """
        Returns the user's active subscription or returns None in any other
        scenario.
        """

        try:
            return self.subscriptions.get(active=True)
        except ObjectDoesNotExist:
            return None
        except MultipleObjectsReturned:
            logger.error('User %s has multiple active subscriptions', self)
            return None
    @property
    def cancel_subscription(self):
        """
        Return user cancel subscription and not expired yet.
        """
        try:
            return self.subscriptions.get(active=True, cancellation=True, expiration__date__gt =  datetime.now().date())
        except ObjectDoesNotExist:
            return None
        except MultipleObjectsReturned:
            logger.error('User %s has multiple active subscriptions', self)
            return None



    @property
    def preview_image(self):
            return self.avatar.url if self.avatar else '/static/images/user.jpeg'