from rest_framework import serializers
from models import Email, EmailAccount


class EmailSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField()
    html = serializers.CharField()
    to = serializers.CharField()
    frm = serializers.CharField()
    subject = serializers.CharField()
    #date = serializers.DateTimeField()
    account_url = serializers.HyperlinkedRelatedField(source='account',
            lookup_field='address',
            view_name='email-account-detail',
            read_only=True)
    account = serializers.SlugRelatedField(read_only=True, slug_field='address')


    class Meta:
        model = Email
        fields = ('url', 'id', 'frm', 'to', 'subject', 'text', 'html', 'attachments', 'account_url', 'account', 'created_at')


class EmailIdSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)


class EmailAccountIdSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='email-account-detail', lookup_field='address')
    emails = serializers.HyperlinkedRelatedField(many=True, view_name='email-detail', read_only=True)

    class Meta:
        model = EmailAccount
        fields = ('url','address', 'callback_url', 'emails')


class EmailAccountSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='email-account-detail', lookup_field='address')
    emails = serializers.HyperlinkedRelatedField(many=True, view_name='email-detail', read_only=True)

    class Meta:
        model = EmailAccount
        fields = ('url','address', 'callback_url', 'emails')
