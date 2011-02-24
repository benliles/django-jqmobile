from django.conf import settings
from django.conf.urls.defaults import patterns, url



urlpatterns = patterns('jqmobile.views',
    url('^$', 'base', name='jqmobile-base',
        kwargs={'slug':settings.JQMOBILE_BASE_IDENTIFIER}),
    url('^(?P<slug>[\w\-_]{1,64})/$', 'base',
        name='jqmobile-ajax-panel'),
)
