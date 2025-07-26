from django.core.cache import cache
from .models import Property
import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

def get_all_properties():
    properties = cache.get('all_properties')
    if properties is None:
        properties = list(Property.objects.all().values(
            'id', 'title', 'description', 'price', 'location', 'created_at'
        ))
        cache.set('all_properties', properties, timeout=3600)  # 1 hour
    return properties

def get_redis_cache_metrics():
    # Connect to Redis
    redis_conn = get_redis_connection("default")

    # Get Redis INFO stats
    info = redis_conn.info()

    # Get hit and miss counts
    hits = info.get('keyspace_hits', 0)
    misses = info.get('keyspace_misses', 0)

    # Calculate hit ratio safely
    total_requests = hits + misses
    hit_ratio = (hits / total_requests) if total_requests > 0 else 0

    # Log the metrics
    logger.info(f"Redis Cache Metrics — Hits: {hits}, Misses: {misses}, Hit Ratio: {hit_ratio}")

    return {
        "hits": hits,
        "misses": misses,
        "hit_ratio": hit_ratio
    }
