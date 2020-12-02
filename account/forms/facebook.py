from django import forms

class FormFacebook(forms.Form):
    """
    Validate the facebook fields
    """

    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    birthday = forms.DateField(required=False)
    avatar = forms.ImageField(required=False)