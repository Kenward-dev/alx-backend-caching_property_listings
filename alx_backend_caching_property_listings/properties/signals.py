from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property

@receiver([post_save, post_delete], sender=Property)
def clear_property_cache(sender, instance, **kwargs):
    """
    Clear the cache for property listings when a Property instance is saved or deleted.
    """
    cache_key = 'all_properties'
    cache.delete(cache_key)
    print(f"Cache cleared for key: {cache_key}")