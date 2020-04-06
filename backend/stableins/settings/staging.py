from .prod import *  # pyflakes:ignore # noqa

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

DEBUG = False

STAGE_ENV = 'staging'

ALLOWED_HOSTS = (
    "api.staging.stableins.com",
)

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'

# Set the pdf generation system on debug mode
# - watermarking
# - Use fake data
PDF_DEBUG = True

# Sentry
sentry_sdk.init(
    dsn="https://3752bd3af5a14f2ea47bd022c5087863@sentry.io/1389585",
    integrations=[
        DjangoIntegration(),
        CeleryIntegration()
    ]
)

# STRIPE
STRIPE_LIVE_MODE = False
STRIPE_PUBLIC_KEY = STRIPE_LIVE_PUBLIC_KEY if STRIPE_LIVE_MODE else STRIPE_TEST_PUBLIC_KEY
STRIPE_SECRET_KEY = STRIPE_LIVE_SECRET_KEY if STRIPE_LIVE_MODE else STRIPE_TEST_SECRET_KEY

# Plaid
PLAID_ENV = "sandbox"

# HelloSign
HELLOSIGN_CLIENTID = env("HELLOSIGN_CLIENTID_STAG")

FRONTEND_URL = "app.staging.stableins.com"

CORS_ORIGIN_WHITELIST = [
    "app.staging.stableins.com",
    "http://app.staging.stableins.com",
    "https://app.staging.stableins.com",
]
# Try to import local settings, if exists
try:
    EXTRA_APPS = ()
    from local import *  # pyflakes:ignore # noqa
    if EXTRA_APPS:
        INSTALLED_APPS = INSTALLED_APPS + EXTRA_APPS
except ImportError:
    pass
