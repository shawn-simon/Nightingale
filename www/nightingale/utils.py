import simplejson

def jsonencoder(obj):
    """Needed to encode complex objects for JSON reponses"""
    if(hasattr(obj, '__dict__')):
        return obj.__dict__
    return None
    
def tojson(obj):
    return simplejson.dumps(obj, default=jsonencoder)
