from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from cheers.apps.account.forms.user_admin import FormAccountUserAdmin
from cheers.apps.account.forms.user_change import FormAccountUserChange
from cheers.apps.account.models import ModelAccountUser, ModelAccountVerification, ModelAccountReference


# -------------------------------------------------------------------------------
# AdminAccountUser
# -------------------------------------------------------------------------------
@admin.register(ModelAccountUser)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = FormAccountUserChange
    add_form =  FormAccountUserAdmin

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'phone_number',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('phone_number',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

@admin.register(ModelAccountVerification)
class AdminAccountVerification(admin.ModelAdmin):
    pass


@admin.register(ModelAccountReference)
class AdminAccountReference(admin.ModelAdmin):
    pass