from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validate_edu_email_address(value):
    if not value.endswith('@surialabs.com'):
        raise forms.ValidationError("Only @surialabs.com emails allowed")
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(
        max_length=254,
        validators=[validate_edu_email_address],
        help_text='Required. Inform a valid email address.'
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')