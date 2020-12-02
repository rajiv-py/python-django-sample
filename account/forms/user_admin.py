from django import forms

from cheers.apps.account.models import ModelAccountUser


class FormAccountUserAdmin(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control required'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control required'}))


    class Meta:
        model = ModelAccountUser
        fields = ('email', 'phone_number')

    # def clean_password2(self):
    #     # Check that the two password entries match
    #     password = self.cleaned_data.get("password")
    #     confirm_password = self.cleaned_data.get("confirm_password")
    #     if password and confirm_password and password != confirm_password:
    #         raise forms.ValidationError("Passwords don't match")
    #     return confirm_password

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.is_bar_owner = True
            user.save()
        return user