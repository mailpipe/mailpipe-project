from django.conf.urls import include, url
from django.urls import path

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from rest_framework.authtoken.views import obtain_auth_token
from mailpipe.views import EmailDetail, EmailAccountDetail, EmailAccountList, EmailList, Attachment, home
from rest_framework.urlpatterns import format_suffix_patterns


from django.contrib import admin

admin.autodiscover()
urlpatterns = [
    #url(r'^admin/',eadmin.site.urls),
    url(r'^$', home, name='home'),
    url(r'^emails/$', EmailList.as_view(), name='email-list'),
    url(r'^emails/(?P<pk>[0-9]+)/$', EmailDetail.as_view(), name='email-detail'),
    url(r'^emails/(?P<email_pk>[0-9]+)/attachments/(?P<content_id>[^/]+)/(?P<name>[^/]+)$',
        never_cache(Attachment.as_view()), name='email-attachment'),
    url(r'^accounts/$', EmailAccountList.as_view(), name='email-account-list'),
    url(r'^accounts/(?P<address>[^/]+)/$', EmailAccountDetail.as_view(), name='email-account-detail'),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),


    url(r'^get_token/$', obtain_auth_token, name='get_token'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

