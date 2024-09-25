from ..used_in_other_config import env

# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # https://github.com/jazzband/django-redis#memcached-exceptions-behavior
            "IGNORE_EXCEPTIONS": env.bool("CACHE_IGNORE_EXCEPTIONS", default=False),
            # This can be used as a good circuit breaker to disable cache connections
            # and make things just fall back to the DB. This can be dangerous though as
            # load on the DB will increase significantly.
        },
    },
}
