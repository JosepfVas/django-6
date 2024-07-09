import secrets
import random
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView, UpdateView
from config.settings import EMAIL_HOST_USER
from users.forms import UsersForm, PasswordRecoveryForm, UserUpdateForm
from users.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin


class UserCreateView(CreateView):
    model = User
    form_class = UsersForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Подтвердите почту перйда по ссылке {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_confirmation(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class PasswordRecoveryView(FormView):
    template_name = 'password_recovery.html'
    form_class = PasswordRecoveryForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = get_object_or_404(User, email=email)
        except User.DoesNotExist:
            # Если пользователя с таким email нет, возвращаем ошибку
            form.add_error('email', 'Пользователь с таким email не существует')
            return super().form_invalid(form)

        new_password = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=10))

        user.password = make_password(new_password)
        user.save()

        send_mail(
            subject='Восстановление пароля',
            message=f'Ваш новый пароль: {new_password}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )

        return super().form_valid(form)


class UserUpdateView(PermissionRequiredMixin, UpdateView):
    model = User
    template_name = "users_app/update_user.html"
    form_class = UserUpdateForm
    permission_required = ("users.can_deactivate_user",)
    success_url = reverse_lazy("users:users_list")
