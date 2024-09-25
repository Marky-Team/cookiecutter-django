from ..used_in_other_config import env

# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d "
            "%(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": env("LOG_LEVEL", default="INFO"), "handlers": ["console"]},
    "loggers": {},
}
if env.bool("SUPRESS_NON_ERROR_DB_ERRORS", default=True):
    LOGGING["loggers"]["django.db.backends"] = {
        "level": "ERROR",
        "handlers": ["console"],
        "propagate": False,
    }
if env.bool("SENTRY_DSN", default=False):
    LOGGING["loggers"]["django.db.backends"] = {
        "level": "ERROR",
        "handlers": ["console"],
        "propagate": False,
    }
if env.bool("DISABLE_DISALLOWED_HOST_WARNINGS", default=True):
    LOGGING["loggers"]["django.security.DisallowedHost"] = {
        "level": "ERROR",
        "handlers": ["console"],
        "propagate": False,
    }
