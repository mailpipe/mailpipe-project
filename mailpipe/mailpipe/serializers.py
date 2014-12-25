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
    #attachments = serializers.HyperlinkedRelatedField()
    account_url = serializers.HyperlinkedRelatedField(source='account',
            lookup_field='address',
            view_name='email-account-detail',
            read_only=True)
    account = serializers.SlugRelatedField(read_only=True, slug_field='address')


    class Meta:
        model = Email
        exclude = ('message', )


class EmailIdSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)


class EmailAccountIdSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='email-account-detail', lookup_field='address')
    emails = serializers.HyperlinkedRelatedField(source='emails', many=True, view_name='email-detail', read_only=True)

    class Meta:
        model = EmailAccount
        fields = ('url','address', 'callback_url')


class EmailAccountSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='email-account-detail', lookup_field='address')
    emails = serializers.HyperlinkedRelatedField(source='emails', many=True, view_name='email-detail', read_only=True)

    class Meta:
        model = EmailAccount
        fields = ('url','address', 'callback_url', 'emails')
