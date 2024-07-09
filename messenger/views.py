import random
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from blog.models import Blog
from client.models import Client
from messenger.forms import MessageForm, MailingForm, MailingChangeStatusForm
from messenger.models import Message, Mailing
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseBadRequest
from messenger.utils import send_mailing
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='moder'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('messenger:message_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user
        self.object.owner = user

        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='moder') and user != self.object.owner:
            raise PermissionDenied
        else:
            return self.object


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('messenger:message_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and user != self.object.owner:
            raise PermissionDenied
        else:
            return self.object


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('messenger:message_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and user != self.object.owner:
            raise PermissionDenied
        else:
            return self.object


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    form_class = MailingForm

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='moder'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('messenger:message_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # if not self.request.user.is_superuser:
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        """Добавление владельца рассылке"""
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    form_class = MailingForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='moder') and user != self.object.owner:
            raise PermissionDenied
        else:
            return self.object


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='moder') and user != self.object.owner:
            raise PermissionDenied
        else:
            return self.object


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    form_class = MailingForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and user != self.object.owner:
            raise PermissionDenied
        else:
            return self.object


class MailingsChangeStatusView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    template_name = "mailings_app/mailing_change_status.html"
    form_class = MailingChangeStatusForm
    success_url = reverse_lazy("messenger:mailing_list")
    permission_required = ("messenger.can_change_status",)


def send_newsletter(request, newsletter_id):
    try:  # Вызываем функцию для отправки рассылки
        send_mailing()
        return HttpResponse("Рассылка отправлена успешно!")
    except Exception as e:
        return HttpResponseBadRequest(f'Ошибка при отрпавке рассылки {e}')


def home(request):
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status=Mailing.STARTED).count()
    unique_clients = Client.objects.distinct().count()

    # Получение случайных трех статей из блога
    blog_posts = list(Blog.objects.all())
    random_articles = random.sample(blog_posts, 3) if len(blog_posts) >= 3 else blog_posts

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_clients': unique_clients,
        'random_articles': random_articles
    }
    return render(request, 'messenger/home.html', context)
