from django import forms

# from passwords.validators import ComplexityValidator
# from passwords.validators import LengthValidator
#

#-------------------------------------------------------------------------------
# FormAccountChangePassword
#-------------------------------------------------------------------------------
class FormAccountChangePassword(forms.Form):
    """
    Form used to change the password of a user's account when they have 
    forgotten their passwords or for security purposes.
    """
    
    password = \
    forms.CharField(label='Password', widget=forms.PasswordInput,
                    # validators=[ComplexityValidator(PASSWORD_COMPLEXITY),
                    #             LengthValidator(min_length=PASSWORD_MIN_LENGTH),
                    #             LengthValidator(max_length=PASSWORD_MAX_LENGTH)]
                   )

    confirm_password = forms.CharField(label='Confirm Password', 
                                       widget=forms.PasswordInput)
    
    #---------------------------------------------------------------------------
    # __init__
    #---------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):

        if kwargs.get('request'):
            self.request = kwargs.pop('request')
            
        super(FormAccountChangePassword, self).__init__(*args,**kwargs)
    
    #---------------------------------------------------------------------------
    # clean_confirm_password
    #---------------------------------------------------------------------------
    def clean_confirm_password(self):
        """
        Checks the new password, raises an error if both the passwords don't 
        match.
        """
        
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")        
        
        if password != confirm_password:  
            raise forms.ValidationError("Passwords do not match.")
        
        if len(password) < 8:
            raise forms.ValidationError('Password is too short.')
        
        if len(password) > 22:
            raise forms.ValidationError('Password is too long.')
        
        return confirm_password   

#     #---------------------------------------------------------------------------
#     # clean_old_password
#     #---------------------------------------------------------------------------
#     def clean_old_password(self):
#         """
#         """
#         old_password = self.cleaned_data.get("old_password")
#         
#         if(not self.request.user.check_password(old_password)):
#             raise forms.ValidationError("Incorrect Password")
#         
#         return old_password
        