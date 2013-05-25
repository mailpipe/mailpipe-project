from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from mailpipe.views import EmailDetail, EmailAccountDetail, EmailAccountList, EmailList, Attachment
from rest_framework.urlpatterns import format_suffix_patterns


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'mailpipe.views.home', name='home'),
    url(r'^emails/$', EmailList.as_view(), name='email-list'),
    url(r'^emails/(?P<pk>[0-9]+)/$', EmailDetail.as_view(), name='email-detail'),
    url(r'^emails/(?P<email_pk>[0-9]+)/attachments/(?P<content_id>[^/]+)/(?P<name>[^/]+)$',
        Attachment.as_view(), name='email-attachment'),
    url(r'^accounts/$', EmailAccountList.as_view(), name='email-account-list'),
    url(r'^accounts/(?P<address>[^/]+)/$', EmailAccountDetail.as_view(), name='email-account-detail'),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^get_token/', 'rest_framework.authtoken.views.obtain_auth_token', name='get_token'),
)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'xml', 'api'])

try:
    from local_urls import urlpatterns
except ImportError as e:
    print('Could not load local_urls.py:')
    print(e)
