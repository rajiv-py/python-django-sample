from phonenumber_field.formfields import PhoneNumberField

from cheers.apps.account.models import ModelAccountUser
from django import forms

class FormAccountProfile(forms.ModelForm):
    """
    This form handle the profile of the user.
    """

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control required'}))

    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control required'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control required'}))
    date_of_birth = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control required'}))
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'form-control required'}))



    class Meta:
        model = ModelAccountUser
        fields = ['email', 'date_of_birth', 'name', 'avatar', 'phone_number', 'address']