from django.contrib.auth.forms import UserCreationForm
from client.forms import StyleFormMixin
from users.models import User
from django import forms


class UsersForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class PasswordRecoveryForm(StyleFormMixin, forms.Form):
    email = forms.EmailField(label='Адрес электронной почты')


class UserUpdateForm(StyleFormMixin):
    class Meta:
        model = User
        fields = ("is_active",)
