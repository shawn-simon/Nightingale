
def jsonencode(obj):
    """Needed to encode complex objects for JSON reponses"""
    if(hasattr(obj, '__dict__')):
        return obj.__dict__
    return None