from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from models import Email, EmailAccount
from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import permissions
from rest_framework import authentication
import serializers

def home(request, *args, **kwargs):
    emails = Email.objects.filter(account__address='test')
    return render(request, 'index.html', {'emails': emails})


class IsEmailAccountOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        return obj.owner == request.user


class EmailAccountList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsEmailAccountOwner,)
    model = EmailAccount
    serializer_class = serializers.EmailAccountIdSerializer

    def pre_save(self, obj):
        obj.owner = self.request.user

    def get_queryset(self):
        return EmailAccount.objects.filter(owner=self.request.user)

    def get_template_names(self):
        return ['email-account-list.html']


class EmailAccountDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsEmailAccountOwner,)
    model = EmailAccount
    serializer_class = serializers.EmailAccountSerializer
    slug_url_kwarg = 'address'
    slug_field = 'address'

    def get_template_names(self):
        return ['email-account-detail.html']

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        return obj.account.owner == request.user


class EmailDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    model = Email
    serializer_class = serializers.EmailSerializer

    def get_template_names(self):
        return ['email-account-email.html']

    def get_queryset(self):
        return Email.objects.filter(account__owner=self.request.user)

