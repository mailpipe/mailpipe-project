from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from mailpipe.views import EmailDetail, EmailAccountDetail, EmailAccountList
from rest_framework.urlpatterns import format_suffix_patterns


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'mailpipe.views.home', name='home'),
    url(r'^email/(?P<pk>[0-9]+)$', EmailDetail.as_view(), name='email-detail'),
    url(r'^accounts$', EmailAccountList.as_view()),
    url(r'^accounts/(?P<address>[a-zA-Z0-9-_@.]+)$', EmailAccountDetail.as_view(), name='email-account-detail'),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^get_token/', 'rest_framework.authtoken.views.obtain_auth_token', name='get_token'),
)

urlpatterns = format_suffix_patterns(urlpatterns)


try:
    from local_urls import urlpatterns
except ImportError as e:
    print('Could not load local_urls.py:')
    print(e)
