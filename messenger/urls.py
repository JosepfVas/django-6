from django.urls import path
from django.views.decorators.cache import cache_page

from messenger.services import send_letters
from messenger.views import MessageListView, MessageCreateView, MessageDetailView, MessageUpdateView, MessageDeleteView, \
    send_newsletter, MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView, MailingDetailView, \
    MailingsChangeStatusView, home


urlpatterns = [
    # Messenger URLS
    path('message/list/', MessageListView.as_view(), name='message_list'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/detail/', MessageDetailView.as_view(), name='message_detail'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    path('send_letters/<int:pk>/', send_letters, name='send_letters'),

    # Mailings URLS
    path('mailing/list/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/<int:pk>/detail/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path("mailing_change_status/<int:pk>/", MailingsChangeStatusView.as_view(), name="mailings_change_status"),

    # Home page
    path('home-page/', cache_page(60)(home), name='home'),

]
