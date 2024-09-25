from ..used_in_other_config import IS_IN_TEST
from ..used_in_other_config import env

# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("MyMarky Engineering", "engineering@mymarky.ai")]

# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
if IS_IN_TEST:
    EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
else:
    EMAIL_BACKEND = env(
        "DJANGO_EMAIL_BACKEND",
        default="django.core.mail.backends.smtp.EmailBackend",
    )

    # https://docs.djangoproject.com/en/dev/ref/settings/#email-host
    EMAIL_HOST = env("EMAIL_HOST", default="mailpit")

    # https://docs.djangoproject.com/en/dev/ref/settings/#email-port
    EMAIL_PORT = 1025

    # https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
    EMAIL_TIMEOUT = 5
