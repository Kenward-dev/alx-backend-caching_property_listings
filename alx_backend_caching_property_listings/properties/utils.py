from django.core.cache import cache
from .models import Property
import time
from django_redis import get_redis_connection
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    """
    Retrieves all properties from the cache or database.
    If properties are not in the cache, they are fetched from the database and cached.
    """
    properties = cache.get('all_properties')
    
    if not properties:
        print("Cache miss. Fetching from database...")
        time.sleep(3)
        properties = Property.objects.all()
        cache.set('all_properties', properties, 3600)
    
    metrics = get_redis_cache_metrics()
    logger.info(f"Cache Metrics: {metrics}")
    return properties

def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.
    
    Returns:
        dict: Dictionary containing cache metrics including hits, misses, and hit ratio
    """
    try:
        redis_connection = get_redis_connection("default")
        
        redis_info = redis_connection.info()
        
        keyspace_hits = redis_info.get('keyspace_hits', 0)
        keyspace_misses = redis_info.get('keyspace_misses', 0)
        
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = (keyspace_hits / total_requests) if total_requests > 0 else 0.0
        
        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total_requests': total_requests,
            'hit_ratio': hit_ratio,
            'hit_percentage': hit_ratio * 100,
            'miss_percentage': (1 - hit_ratio) * 100 if total_requests > 0 else 0.0
        }
        
        logger.info(f"Redis Cache Metrics: "
                   f"Hits: {keyspace_hits}, "
                   f"Misses: {keyspace_misses}, "
                   f"Hit Ratio: {hit_ratio:.4f} ({hit_ratio * 100:.2f}%)")
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {str(e)}")
        return {
            'error': str(e),
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'total_requests': 0,
            'hit_ratio': 0.0,
            'hit_percentage': 0.0,
            'miss_percentage': 0.0
        }