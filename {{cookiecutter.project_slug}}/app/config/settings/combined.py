# ruff: noqa: ERA001, E501, F403, I001
"""
This is the file you should generally use as your "settings" file; this one combines all the others in an appropriate
order.
"""

# Common settings
from .used_in_other_config import *

# Django Core Settings
from .django.core_cache import *
from .django.core_database import *
from .django.core_debugging import *
from .django.core_email import *
from .django.core_file_uploads import *
from .django.core_forms import *
from .django.core_globalization import *
from .django.core_http import *
from .django.core_logging import *
from .django.core_models import *
from .django.core_security import *
from .django.core_templates import *
from .django.core_testing import *
from .django.core_urls import *

# Django Contrib App Settings
from .django.contrib_admin import *
from .django.contrib_auth import *
from .django.contrib_sessions import *
from .django.contrib_sites import *
from .django.contrib_static import *

# Libraries settings
from .libraries.allauth import *
from .libraries.anymail import *
from .libraries.celery import *
from .libraries.cors_headers import *
from .libraries.crispy_forms import *
from .libraries.debug_toolbar import *
from .libraries.djangorestframework_simplejwt import *
from .libraries.drf_spectacular import *
from .libraries.rest_framework import *
from .libraries.sentry import *

# Services settings

# Our application settings
from .custom import *
