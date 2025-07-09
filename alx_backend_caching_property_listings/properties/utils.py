from django.core.cache import cache
from .models import Property

def get_all_properties():
    """
    Retrieves all properties from the cache or database.
    If properties are not in the cache, they are fetched from the database and cached.
    """
    properties = cache.get('all_properties')
    
    if not properties:
        properties = Property.objects.all()
        cache.set('all_properties', properties, 3600)
    
    return properties