from django.forms import ModelForm, ModelChoiceField, BooleanField
from client.forms import StyleFormMixin
from client.models import Client
from messenger.models import Message, Mailing


class MessageForm(ModelForm, StyleFormMixin):
    class Meta:
        model = Message
        fields = ['subject', 'body']


class MailingForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing
        exclude = ('owner', 'status')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        if self.request:
            user = self.request.user
            self.fields["client"].queryset = Client.objects.filter(owner=user)
            self.fields["message"].queryset = Message.objects.filter(owner=user)


class MailingChangeStatusForm(StyleFormMixin):
    class Meta:
        model = Mailing
        fields = ("status",)
