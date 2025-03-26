from ..used_in_other_config import APPS_DIR
from ..used_in_other_config import ENABLE_DEBUG_TOOLBAR

# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = [
    # DJANGO APPS
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.forms",
    # THIRD PARTY APPS
    "crispy_forms",
    "crispy_bootstrap5",
    "allauth",
    "allauth.account",
    "allauth.mfa",
    "allauth.socialaccount",
    "anymail",
{%- if cookiecutter.use_celery == 'y' %}
    "django_celery_beat",
    "django_celery_results",
{%- endif %}
{%- if cookiecutter.use_drf == "y" %}
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "drf_spectacular",
{%- endif %}
{%- if cookiecutter.frontend_pipeline == 'Webpack' %}
    "webpack_loader",
{%- elif cookiecutter.frontend_pipeline == 'Django Compressor' %}
    "compressor",
{%- endif %}
    "django_extensions",
    # LOCAL APPS
    "{{cookiecutter.python_package_name}}",
    "{{cookiecutter.python_package_name}}.users",
    # Your stuff: custom apps go here
]
if ENABLE_DEBUG_TOOLBAR:
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
    INSTALLED_APPS += ["debug_toolbar"]

# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {"sites": "{{cookiecutter.python_package_name}}.contrib.sites.migrations"}
