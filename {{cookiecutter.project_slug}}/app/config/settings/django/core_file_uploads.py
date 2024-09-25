from config.settings.used_in_other_config import APPS_DIR
from config.settings.used_in_other_config import env

if env.bool("USE_S3", default=False):
    _AWS_EXPIRY = 60 * 60 * 24 * 7

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "bucket_name": env("DJANGO_AWS_STORAGE_BUCKET_NAME"),
                "object_parameters": {
                    "CacheControl": f"max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, "
                    f"must-revalidate",
                },
                "max_memory_size": env.int(
                    "DJANGO_AWS_S3_MAX_MEMORY_SIZE",
                    default=100_000_000,  # 100MB
                ),
                "location": "media",
                "file_overwrite": False,
            },
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

else:
    # https://docs.djangoproject.com/en/dev/ref/settings/#media-root
    MEDIA_ROOT = str(APPS_DIR / "media")

    # https://docs.djangoproject.com/en/dev/ref/settings/#media-url
    MEDIA_URL = "/media/"
