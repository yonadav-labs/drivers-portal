import os

import pytest

import django
from django.conf import settings

# We manually designate which settings we will be using in an environment variable
# This is similar to what occurs in the `manage.py`
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stableins.settings.tests')

# `pytest` automatically calls this function once when tests are run.
def pytest_configure():
    settings.DEBUG = True
    # If you have any test specific settings, you can declare them here,
    # e.g.
    # settings.PASSWORD_HASHERS = (
    #     'django.contrib.auth.hashers.MD5PasswordHasher',
    # )
    django.setup()
    # Note: In Django =< 1.6 you'll need to run this instead
    # settings.configure()

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass

# https://docs.pytest.org/en/latest/writing_plugins.html?highlight=writing%20plugins#requiring-loading-plugins-in-a-test-module-or-conftest-file
pytest_plugins = [
    "tests.quotes.fixtures",
]
