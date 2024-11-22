from django.core.cache import cache
import logging

logger = logging.getLogger('myapp')

def log_cache_hit_miss(key):
    if cache.get(key):
        logger.info(f"Cache hit for key: {key}")
    else:
        logger.info(f"Cache miss for key: {key}")