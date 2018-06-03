import uuid

import pytest

from miles import create_app


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SECRET_KEY': 'test_secret_key',
    })

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client
        self.code = None

    def login(self):
        from miles.models import User
        code = str(uuid.uuid4())
        User(
            name='some_user',
            email='some_user@email.com',
            card_number=1234567890,
            code=code,
        ).save()
        return self._client.post(
            '/login',
            json={'code': code}
        )


@pytest.fixture
def auth(client):
    return AuthActions(client)
