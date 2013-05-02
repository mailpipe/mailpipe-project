from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from models import Email, Route
from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import permissions
from rest_framework import authentication
from serializers import EmailSerializer, RouteIdSerializer, RouteSerializer


def home(request, *args, **kwargs):
    emails = Email.objects.filter(route__name='test')
    return render(request, 'index.html', {'emails': emails})


class IsRouteOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        return obj.owner == request.user


class RouteList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsRouteOwner,)
    model = Route
    serializer_class = RouteIdSerializer

    def pre_save(self, obj):
        obj.owner = self.request.user

    def get_queryset(self):
        return Route.objects.filter(owner=self.request.user)

    def get_template_names(self):
        return ['route-list.html']


class RouteDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsRouteOwner,)
    model = Route
    serializer_class = RouteSerializer
    slug_url_kwarg = 'name'
    slug_field = 'name'

    def get_template_names(self):
        return ['route-detail.html']

class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        return obj.route.owner == request.user


class EmailDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    model = Email
    serializer_class = EmailSerializer

    def get_template_names(self):
        return ['route-email.html']

    def get_queryset(self):
        return Email.objects.filter(route__owner=self.request.user)

