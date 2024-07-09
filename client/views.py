from django.shortcuts import render
from client.models import Client
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy, reverse
from client.forms import ClientForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='moder'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client:client_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user
        self.object.owner = user

        return super().form_valid(form)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='moder') and user != self.object.owner:
            raise PermissionDenied
        else:
            return self.object


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    success_url = reverse_lazy('client:client_list')
    form_class = ClientForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and user != self.object.owner:
            raise PermissionDenied
        else:
            return self.object


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('client:client_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and user != self.object.owner:
            raise PermissionDenied
        else:
            return self.object