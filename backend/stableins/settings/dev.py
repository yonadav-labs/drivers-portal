from .common import *  # pyflakes:ignore # noqa

DEBUG = True

STAGE_ENV = 'development'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Try to import local settings, if exists
try:
    EXTRA_APPS = ()
    from local import *  # pyflakes:ignore # noqa
    if EXTRA_APPS:
        INSTALLED_APPS = INSTALLED_APPS + EXTRA_APPS
except ImportError:
    pass

# STRIPE
STRIPE_PUBLIC_KEY = STRIPE_LIVE_PUBLIC_KEY if STRIPE_LIVE_MODE else STRIPE_TEST_PUBLIC_KEY
STRIPE_SECRET_KEY = STRIPE_LIVE_SECRET_KEY if STRIPE_LIVE_MODE else STRIPE_TEST_SECRET_KEY

# Plaid
PLAID_ENV = "sandbox"

# HelloSign
HELLOSIGN_CLIENTID = env("HELLOSIGN_CLIENTID_DEV")

LOCALTUNNEL_DOMAIN = "{}.localtunnel.me".format(env('DEV_LOCALTUNNEL_SUB'))
ALLOWED_HOSTS = ['localhost', LOCALTUNNEL_DOMAIN]

# Anymail - Sendgrid - Development
ANYMAIL_SENDGRID_SEND_DEFAULTS = {
    "esp_extra": {
        "mail_settings": {
            "sandbox_mode": {
                "enable": True
            }
        }
    }
}

CORS_ORIGIN_WHITELIST = [
    "localhost:8080",
]