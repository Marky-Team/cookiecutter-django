from config.settings.used_in_other_config import env

ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)

# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = "username"

# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_EMAIL_REQUIRED = True

{%- if cookiecutter.username_type == "email" %}
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_USERNAME_REQUIRED = False
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
{%- endif %}

# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_ADAPTER = "users.adapters.AccountAdapter"

# https://docs.allauth.org/en/latest/account/forms.html
ACCOUNT_FORMS = {"signup": "users.forms.UserSignupForm"}

# https://docs.allauth.org/en/latest/socialaccount/configuration.html
SOCIALACCOUNT_ADAPTER = "users.adapters.SocialAccountAdapter"

# https://docs.allauth.org/en/latest/socialaccount/configuration.html
SOCIALACCOUNT_FORMS = {"signup": "users.forms.UserSocialSignupForm"}
