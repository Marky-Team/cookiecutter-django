{% if cookiecutter.use_drf == "y" -%}
from corsheaders.defaults import default_headers

# django-cors-headers - https://github.com/adamchainz/django-cors-headers?tab=readme-ov-file#configuration
CORS_URLS_REGEX = r"^/api/.*$"
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = (
    *default_headers,
    "x-business-id",
    "baggage",
    "sentry-trace",
)
{% endif -%}
