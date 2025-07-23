from django.core.cache import cache
from django_redis import get_redis_connection


class CoreCacheMixin:
    CACHE_KEY_PREFIX: str
    CACHE_TTL: int = 60 * 5

    def _cache_get_or_set(self, key, value):
        return cache.get_or_set(
            key=f"{self.CACHE_KEY_PREFIX}::{key}",
            default=value,
            timeout=self.CACHE_TTL,
        )

    def _cache_destroy(self, key):
        cache.delete(f"{self.CACHE_KEY_PREFIX}::{key}")

    def _cache_destroy_key_wild(self, key):
        redis_conn = get_redis_connection("default")
        if key := redis_conn.keys(f"{self.CACHE_KEY_PREFIX}::{key}::*"):
            redis_conn.delete(*key)

    def _cache_destroy_prefix_wild(self):
        redis_conn = get_redis_connection("default")
        if key := redis_conn.keys(f"{self.CACHE_KEY_PREFIX}::*"):
            redis_conn.delete(*key)
