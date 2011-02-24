from django.conf import settings
from django.http import HttpResponse, Http404
from django.template import loader, RequestContext

from jqmobile.models import Page



def base(request, slug, **kwargs):
    kwargs.setdefault('template_name','jqmobile/base.html')
    kwargs.setdefault('template_loader', loader)
    kwargs.setdefault('extra_context', {})
    kwargs.setdefault('context_processors',None)
    kwargs.setdefault('template_object_name', 'page')
    kwargs.setdefault('mimetype',None)
    
    try:
        page = Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        raise Http404('%s does not resolve to a page' % (str(slug),))
    
    context = RequestContext(request, {kwargs['template_object_name']: page,},
                             kwargs['context_processors'])
    
    for key, value in kwargs['extra_context'].items():
        if callable(value):
            context[key] = value()
        else:
            context[key] = value
    
    return HttpResponse(kwargs['template_loader'].get_template(kwargs['template_name']).render(context),
                        mimetype=kwargs['mimetype'])
