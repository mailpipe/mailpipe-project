from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

from .models import Email, EmailAccount
from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import authentication
from . import serializers
import base64


def home(request, *args, **kwargs):
    emails = Email.objects.filter(account__address='test')
    return render(request, 'index.html', {'emails': emails})


class EmailAccountList(generics.ListCreateAPIView):
    serializer_class = serializers.EmailAccountIdSerializer

    def get_queryset(self):
        return EmailAccount.objects.filter(owner=self.request.user)

    def get_template_names(self):
        return ['email-account-list.html']


class EmailAccountDetail(generics.RetrieveDestroyAPIView):
    serializer_class = serializers.EmailAccountSerializer
    lookup_field = 'address'

    def get_queryset(self):
        return EmailAccount.objects.filter(owner=self.request.user)

    def get_template_names(self):
        return ['email-account-detail.html']


class Attachment(generics.GenericAPIView):
    def get(self, *args, **kwargs):
        email_pk = kwargs['email_pk']
        content_id = kwargs['content_id']
        name = kwargs.get('name', None)
        email = get_object_or_404(Email, pk=email_pk, account__owner=self.request.user)
        attachment = email.raw_attachments()[content_id]
        if not attachment['filename'] == name:
            return redirect('email-attachment',
                            email_pk=email_pk,
                            content_id=content_id,
                            name=attachment['filename'])

        response = HttpResponse(attachment['payload'])
        response['Content-Type'] = attachment['content_type']
        #response['Content-Disposition'] = 'attachment; filename=%s' % attachment['filename']
        return response


class EmailDetail(generics.RetrieveDestroyAPIView):
    serializer_class = serializers.EmailSerializer

    def get_template_names(self):
        return ['email-account-email.html']

    def get_queryset(self):
        return Email.objects.filter(account__owner=self.request.user)

class EmailList(generics.ListAPIView):
    serializer_class = serializers.EmailSerializer

    def get_template_names(self):
        return ['email-account-email-list.html']

    def get_queryset(self):
        return Email.objects.filter(account__owner=self.request.user)

