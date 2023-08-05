import pytest

from .. import factories


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def user():
    return factories.UserFactory()


@pytest.fixture
def auth_client(client, user):
    client.force_login(user)
    return client
