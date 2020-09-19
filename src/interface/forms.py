from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "facebook", "twitter", "sponsorid", "matrixid")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email", "facebook", "twitter", "sponsorid", "matrixid")


class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        Model = User
        fields = ("username", "password")


class SignUpForm(CustomUserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['password1']:
            self.fields[fieldname].help_text = 'At least 8 chars.'
            self.fields[fieldname].initial = 'Password'
        for fieldname in ['password2']:
            self.fields[fieldname].help_text = ''
            self.fields[fieldname].initial = 'Confirm Pass'

    username = forms.CharField(
        max_length=30,
        required=True,
        help_text='Required',
        initial="",
        label="Username",

    )
    email = forms.EmailField(
        max_length=254,
        help_text='Required',
        initial="",
        label="Email"
    )
    matrixid = forms.CharField(
        max_length=30,
        required=False,
        help_text='Optional',
        initial="",
        label="Matrix Id"
    )
    password1 = forms.PasswordInput()
    class Meta:
        model = User
        fields = ("username", "email", "matrixid")


class UserLoginForm(CustomUserLoginForm):

    class Meta:
        model = User
