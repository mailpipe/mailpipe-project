from rest_framework import serializers
from models import Email, EmailAccount


class EmailSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.Field()
    text = serializers.CharField()
    html = serializers.CharField()
    to = serializers.CharField()
    frm = serializers.CharField()
    subject = serializers.CharField()
    date = serializers.DateTimeField()
    attachments = serializers.Field()
    account_url = serializers.HyperlinkedRelatedField(source='account', slug_field='address', view_name='email-account-detail')
    account = serializers.SlugRelatedField(read_only=True, slug_field='address')


    class Meta:
        model = Email



class EmailIdSerializer(serializers.Serializer):
    id = serializers.Field()


class EmailAccountIdSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='email-account-detail', slug_field='address')
    emails = serializers.HyperlinkedRelatedField(source='email_set', many=True, view_name='email-detail')

    class Meta:
        model = EmailAccount
        fields = ('url','address', 'callback_url')


class EmailAccountSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='email-account-detail', slug_field='address')
    emails = serializers.HyperlinkedRelatedField(source='email_set', many=True, view_name='email-detail')

    class Meta:
        model = EmailAccount
        fields = ('url','address', 'callback_url', 'emails')
