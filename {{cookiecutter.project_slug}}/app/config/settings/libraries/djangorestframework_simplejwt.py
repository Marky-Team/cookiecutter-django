from config.settings.used_in_other_config import env

# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
SIMPLE_JWT = {
    "SIGNING_KEY": env.get_value("JWT_SIGNING_KEY", default="NOT_THE_REAL_KEY"),
    "JTI_CLAIM": None,
    "TOKEN_TYPE_CLAIM": None,
    "USER_ID_CLAIM": "sub",
}
