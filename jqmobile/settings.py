from django.conf import settings
from django.core.urlresolvers import get_callable

if 'jqmobile' in settings.INSTALLED_APPS:
    if not hasattr(settings,'JQMOBILE_BASE_IDENTIFIER'):
        settings.JQMOBILE_BASE_IDENTIFIER = 'home'
    
    if not hasattr(settings, 'JQMOBILE_PAGE_RESOLVERS'):
        settings.JQMOBILE_PAGE_RESOLVERS = ('jqmobile.resolvers.page_model_resolver',)
    
    if isinstance(settings.JQMOBILE_PAGE_RESOLVERS, basestring) or callable(settings.JQMOBILE_PAGE_RESOLVERS):
        settings.JQMOBILE_PAGE_RESOLVERS = (settings.JQMOBILE_PAGE_RESOLVERS,)
    
    if not isinstance(settings.JQMOBILE_PAGE_RESOLVERS, (tuple,list,)):
        raise ValueError('JQMOBILE_PAGE_RESOLVERS must be a list or tuple')
    
    settings.JQMOBILE_PAGE_RESOLVERS = map(get_callable,
                                           settings.JQMOBILE_PAGE_RESOLVERS)
    
    for resolver in settings.JQMOBILE_PAGE_RESOLVERS:
        if isinstance(resolver, basestring):
            raise ValueError('%s could not be resolved to a callable' % (resolver,))
