from rest_framework import serializers
from models import Email, Route


class EmailSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.Field()
    text = serializers.CharField()
    html = serializers.CharField()
    to = serializers.CharField()
    frm = serializers.CharField()
    subject = serializers.CharField()
    date = serializers.DateTimeField()
    attachments = serializers.Field()
    route_url = serializers.HyperlinkedRelatedField(source='route', slug_field='name', view_name='route-detail')
    route = serializers.SlugRelatedField(read_only=True, slug_field='name')


    class Meta:
        model = Email



class EmailIdSerializer(serializers.Serializer):
    id = serializers.Field()


class RouteIdSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='route-detail', slug_field='name')
    emails = serializers.HyperlinkedRelatedField(source='email_set', many=True, view_name='email-detail')

    class Meta:
        model = Route
        fields = ('url','name', 'callback_url')


class RouteSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='route-detail', slug_field='name')
    emails = serializers.HyperlinkedRelatedField(source='email_set', many=True, view_name='email-detail')

    class Meta:
        model = Route
        fields = ('url','name', 'callback_url', 'emails')
