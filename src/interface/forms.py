from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "facebook", "twitter", "sponsorid", "matrixid")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "facebook", "twitter", "sponsorid", "matrixid")


class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        Model = CustomUser
        fields = ("username", "password")


class SignUpForm(CustomUserCreationForm):
    username = forms.CharField(max_length=30, required=False, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Not yet required, as I\'m still deciding how to handle mail')
    matrixid = forms.CharField(max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = CustomUser
        fields = ("username", "email", "matrixid")


class UserLoginForm(CustomUserLoginForm):

    class Meta:
        model = CustomUser