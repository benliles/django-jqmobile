try:
    from xml.etree import cElementTree as etree
except ImportError:
    from xml.etree import ElementTree as etree

from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.template import Template, Context
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

from jqmobile.validators import *
from jqmobile.exceptions import CircularError, RenderingError



class BaseTemplate(models.Model):
    attributes = models.CharField(max_length=255, 
                                  validators=[validate_attributes], blank=True)
    title = models.CharField(max_length=255)
    body = models.TextField(validators=[validate_xml, validate_template])
    
    def __unicode__(self):
        return self.title
    
    def render(self, **kwargs):
        return Template(self.body).render(Context(kwargs))
    
    class Meta:
        abstract=True
    
class HeaderTemplate(BaseTemplate):
    class Meta:
        verbose_name = u'Header'

class FooterTemplate(BaseTemplate):
    class Meta:
        verbose_name = u'Footer'

def _render(obj, parents=None, string=True, template='jqmobile/page.html'):
    if parents is None:
        parents = set([])
    if not isinstance(parents, set):
        parents = set(parents)
    
    if obj.hash in parents:
        raise CircularError(parents)
    
    parents.add(obj.hash)
    nodes = []
    
    page = render_to_string(template,{'page':obj,'jqmobile_embed': True})
    try:
        page = etree.fromstring(page)
    except SyntaxError, e:
        print page
        raise e
    
    nodes.append(page)
    try:
        for link in etree.ElementTree(page).findall('//a'):
            if link.get('rel','') == 'external' or link.get('target','') != '':
                continue
            
            href = link.get('href')
            
            if not (href.startswith('http') or href.startswith('/')):
                continue
            
            for resolver in settings.JQMOBILE_PAGE_RESOLVERS:
                result = resolver(href)
                if result is not None:
                    break
            
            if result is None:
                continue
            
            if not getattr(result,'embed',True):
                continue
            
            try:
                if hasattr(result,'render') and callable(result.render):
                    result = result.render(parents=parents)
                else:
                    result = result
                
                if isinstance(result, basestring):
                    nodes.append(result)
                elif ((hasattr(result,'__iter__') and callable(result.__iter__)) or 
                      (hasattr(result,'next') and callable(result.next))):
                    nodes.extend(result)
            except CircularError:
                pass
            
            link.set('href', '#%s' % (href,))
    except:
        from traceback import print_exc
        print_exc()
        pass
    
    if string:
        return '\n'.join(map(lambda n: isinstance(n, basestring) and n or etree.tostring(n),nodes))
    
    return nodes

class Page(models.Model):
    slug = models.SlugField(max_length=64, db_index=True)
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField(validators=[validate_xml])
    attributes = models.CharField(max_length=255,
                                  validators=[validate_attributes], blank=True)
    content_attributes = models.CharField(max_length=255,
                                          validators=[validate_attributes],
                                          blank=True)
    embed = models.BooleanField(default=True)
    sites = models.ManyToManyField(Site, blank=True)
    header_content = models.TextField(validators=[validate_xml], blank=True)
    header_content_attributes = models.CharField(max_length=255,
                                                 validators=[validate_attributes],
                                                 blank=True)
    footer_content = models.TextField(validators=[validate_xml], blank=True)
    footer_content_attributes = models.CharField(max_length=255,
                                                 validators=[validate_attributes],
                                                 blank=True)
    header_template = models.ForeignKey(HeaderTemplate, related_name='pages',
                                        blank=True, null=True)
    footer_template = models.ForeignKey(FooterTemplate, related_name='pages',
                                        blank=True, null=True)
    
    def __unicode__(self):
        if self.title:
            return self.title
        
        return self.slug
    
    @models.permalink
    def get_absolute_url(self):
        return ('jqmobile.views.base', [self.slug])
    
    @property
    def hash(self):
        return self.get_absolute_url()
    
    render = _render
    
    @property
    def header(self):
        if self.header_template:
            return self.header_template.render(page=self)
        
        if self.header_content:
            return self.header_content
        
        return u''
    
    @property
    def footer(self):
        if self.footer_template:
            return self.footer_template.render(page=self)
        
        if self.footer_content:
            return self.footer_content
        
        return u''
    
    @property
    def header_attributes(self):
        if self.header_template and self.header_template.attributes:
            return self.header_template.attributes
        
        if self.header_content_attributes:
            return self.header_content_attributes
    
    @property
    def footer_attributes(self):
        if self.footer_template and self.footer_template.attributes:
            return self.footer_template.attributes
        
        if self.footer_content_attributes:
            return self.footer_content_attributes
    
    
