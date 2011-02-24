from urlparse import urlparse
from django.core.urlresolvers import resolve
from django.http import Http404

from jqmobile.models import Page
from jqmobile.views import base



def page_model_resolver(href):
    try:
        view, args, kwargs = resolve(urlparse(href)[2])
        
        if view != base:
            return None
        
        return Page.objects.get(slug=kwargs['slug'])
    except Page.DoesNotExist:
        return None
    except Exception, e:
        return None
