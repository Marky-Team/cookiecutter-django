import logging

import sentry_sdk
{%- if cookiecutter.use_celery == 'y' %}
from sentry_sdk.integrations.celery import CeleryIntegration
{% endif -%}
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from ..used_in_other_config import env

if env.bool("ENABLE_SENTRY", default=True):
    SENTRY_DSN = env("SENTRY_DSN")

    if SENTRY_DSN:
        SENTRY_LOG_LEVEL = env.int("DJANGO_SENTRY_LOG_LEVEL", logging.INFO)

        sentry_logging = LoggingIntegration(
            level=SENTRY_LOG_LEVEL,  # Capture info and above as breadcrumbs
            event_level=logging.ERROR,  # Send errors as events
        )
        integrations = [
            sentry_logging,
            DjangoIntegration(),
            RedisIntegration(),
            {%- if cookiecutter.use_celery == 'y' %}
            CeleryIntegration(),
            {% endif -%}
        ]
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=integrations,
            environment=env("SENTRY_ENVIRONMENT", default="production"),
            traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE", default=0.0),
        )
