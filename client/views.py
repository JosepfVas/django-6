from django.shortcuts import render
from client.models import Client
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView


class ClientListView(ListView):
    model = Client
