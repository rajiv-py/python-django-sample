from django.db import models

from cheers.apps.account.models import ModelAccountUser
from cheers.apps.base.models.base import ModelAbstractBase


class ModelAccountReference(ModelAbstractBase):
    """
    This model store the references for signup.
    """

    referrer_from = models.ForeignKey(ModelAccountUser, related_name="my_references", on_delete=models.CASCADE)
    referrer_to = models.ForeignKey(ModelAccountUser, related_name="references", on_delete=models.CASCADE)
    code = models.CharField(max_length=20, help_text="The referrer code which are used for signup")

    # -------------------------------------------------------------------------
    # Meta
    # -------------------------------------------------------------------------
    class Meta:
        db_table = "account_reference"
        verbose_name = "Reference"
        verbose_name_plural = "References"

    # ---------------------------------------------------------------------------
    # __str__
    # ---------------------------------------------------------------------------
    def __str__(self):
        """
        Returns the string representation of the user object.
        """

        return self.referrer_from.email