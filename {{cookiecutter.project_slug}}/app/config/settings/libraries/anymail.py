# Anymail
# ------------------------------------------------------------------------------
# https://anymail.readthedocs.io/en/stable/installation/#installing-anymail
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
# https://anymail.readthedocs.io/en/stable/installation/#anymail-settings-reference
{%- if cookiecutter.mail_service == 'Mailgun' %}
# https://anymail.readthedocs.io/en/stable/esps/mailgun/
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
ANYMAIL = {
    "MAILGUN_API_KEY": env("MAILGUN_API_KEY"),
    "MAILGUN_SENDER_DOMAIN": env("MAILGUN_DOMAIN"),
    "MAILGUN_API_URL": env("MAILGUN_API_URL", default="https://api.mailgun.net/v3"),
}
{%- elif cookiecutter.mail_service == 'Amazon SES' %}
# https://anymail.readthedocs.io/en/stable/esps/amazon_ses/
EMAIL_BACKEND = "anymail.backends.amazon_ses.EmailBackend"
ANYMAIL = {}
{%- elif cookiecutter.mail_service == 'Mailjet' %}
# https://anymail.readthedocs.io/en/stable/esps/mailjet/
EMAIL_BACKEND = "anymail.backends.mailjet.EmailBackend"
ANYMAIL = {
    "MAILJET_API_KEY": env("MAILJET_API_KEY"),
    "MAILJET_SECRET_KEY": env("MAILJET_SECRET_KEY"),
}
{%- elif cookiecutter.mail_service == 'Mandrill' %}
# https://anymail.readthedocs.io/en/stable/esps/mandrill/
EMAIL_BACKEND = "anymail.backends.mandrill.EmailBackend"
ANYMAIL = {
    "MANDRILL_API_KEY": env("MANDRILL_API_KEY"),
    "MANDRILL_API_URL": env("MANDRILL_API_URL", default="https://mandrillapp.com/api/1.0"),
}
{%- elif cookiecutter.mail_service == 'Postmark' %}
# https://anymail.readthedocs.io/en/stable/esps/postmark/
EMAIL_BACKEND = "anymail.backends.postmark.EmailBackend"
ANYMAIL = {
    "POSTMARK_SERVER_TOKEN": env("POSTMARK_SERVER_TOKEN"),
    "POSTMARK_API_URL": env("POSTMARK_API_URL", default="https://api.postmarkapp.com/"),
}
{%- elif cookiecutter.mail_service == 'Sendgrid' %}
# https://anymail.readthedocs.io/en/stable/esps/sendgrid/
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
ANYMAIL = {
    "SENDGRID_API_KEY": env("SENDGRID_API_KEY"),
    "SENDGRID_API_URL": env("SENDGRID_API_URL", default="https://api.sendgrid.com/v3/"),
}
{%- elif cookiecutter.mail_service == 'Brevo' %}
# https://anymail.readthedocs.io/en/stable/esps/brevo/
EMAIL_BACKEND = "anymail.backends.brevo.EmailBackend"
ANYMAIL = {
    "BREVO_API_KEY": env("BREVO_API_KEY"),
    "BREVO_API_URL": env("BREVO_API_URL", default="https://api.brevo.com/v3/"),
}
{%- elif cookiecutter.mail_service == 'SparkPost' %}
# https://anymail.readthedocs.io/en/stable/esps/sparkpost/
EMAIL_BACKEND = "anymail.backends.sparkpost.EmailBackend"
ANYMAIL = {
    "SPARKPOST_API_KEY": env("SPARKPOST_API_KEY"),
    "SPARKPOST_API_URL": env("SPARKPOST_API_URL", default="https://api.sparkpost.com/api/v1"),
}
{%- elif cookiecutter.mail_service == 'Other SMTP' %}
# https://anymail.readthedocs.io/en/stable/esps
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
ANYMAIL = {}
{%- endif %}
