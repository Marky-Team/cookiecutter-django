import pytest

from {{cookiecutter.python_package_name}}.users.models import User
from {{cookiecutter.python_package_name}}.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()
