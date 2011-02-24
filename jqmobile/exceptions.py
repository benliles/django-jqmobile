class RenderingError(Exception):
    """ Error rendering the Panel """

class CircularError(RenderingError):
    """ Encountered a circular include """
    
    def __init__(self, chain=[]):
        self.chain = chain
    
    def __unicode__(self):
        return u'Circular include error: %s' % (str(self.chain),)