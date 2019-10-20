import os
import pytest

import django
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manatal_challenge.settings")


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


def pytest_configure():
    settings.DEBUG = False
    django.setup()
