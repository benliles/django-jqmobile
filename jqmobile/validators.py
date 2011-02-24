try:
    from xml.etree import cElementTree as etree
except ImportError:
    from xml.etree import ElementTree as etree

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.template import Template

__all__ = (
    'validate_xml',
    'validate_template',
    'validate_attributes',)

def validate_xml(value):
    value = '<div>' + value + '</div>'
    try:
        etree.fromstring(value)
    except Exception, e:
        print value
        raise ValidationError('Error parsing the xml: %s' % (str(e),))

def validate_template(value):
    try:
        Template(value)
    except Exception, e:
        raise ValidationError('Error parsing the template: %s' % (str(e),))

validate_attributes = RegexValidator(regex=r'^[\w\-]+=\"[\w\d\s]+\"([ \t]+[\w\-]+=\"[\w\d\s]+\")*$',
                                     message='HTML attributes only: key="value"')
