from django.urls import path
from django.views.decorators.cache import cache_page
from client.views import ClientListView, ClientDetailView, ClientUpdateView, ClientCreateView, ClientDeleteView

urlpatterns = [
    path('client/list', ClientListView.as_view(), name='client_list'),
    path('client/create', ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/detail', ClientDetailView.as_view(), name='client_detail'),
    path('client/<int:pk>/update', ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/delete', ClientDeleteView.as_view(), name='client_delete'),

]
