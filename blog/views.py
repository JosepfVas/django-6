from blog.services import get_data_from_cache
from django.shortcuts import render

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from blog.forms import BlogForm
from blog.models import Blog

from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)


class BlogListView(ListView):
    model = Blog

    def get_queryset(self):
        return get_data_from_cache()


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object


class BlogCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy("blog:blog_list")

    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True
        return False


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy("blog:blog_list")

    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True
        return False


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy("blog:blog_list")

    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True
        return False
