from django import forms


#-------------------------------------------------------------------------------
# FormAccountForgotPassword
#-------------------------------------------------------------------------------
from cheers.apps.account.models import ModelAccountUser


class FormAccountForgotPassword(forms.Form):
    """
    Form used to provide the user with the functionality that if the user has 
    forgotten their old password then they can have a new password.
    """
    
    email = forms.EmailField(max_length=60, label='Email')
    

    #---------------------------------------------------------------------------
    # clean
    #---------------------------------------------------------------------------
    def clean(self):
        """
        Only those user accounts exist, are active and have been verified
        are allowed to change their account passwords.
        """
        
        email = self.cleaned_data.get('email')
        
        try:
            self.user = ModelAccountUser.objects.get(email=email)
            
        except ModelAccountUser.DoesNotExist:
            raise forms.ValidationError("The submitted email address was not located within our database.")
        
        if not self.user.is_active:
            raise forms.ValidationError("Sorry! your account is not active.")

        return self.cleaned_data
