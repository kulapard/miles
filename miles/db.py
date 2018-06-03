import uuid

import click
from flask.cli import with_appcontext
from pymodm import connect


@click.command('create-user')
@click.argument('name')
@click.argument('email')
@click.argument('card_number')
@with_appcontext
def create_user(name: str, email: str, card_number: int):
    """Создаёт одно го пользователя с заданныими параметрами"""
    from miles.models import User

    user = User(
        name=name,
        email=email,
        card_number=card_number,
        code=str(uuid.uuid4()),
    ).save()
    print(f"User successfully created! Code: {user.code}")
    return user.code


@click.command('preload-users')
@with_appcontext
def preload_users():
    """Создаёт 10 пользователей в базе"""
    from miles.models import User

    for i in range(10):
        user = User(
            name=f'preloaded_user_{i}',
            email=f'preloaded_user_{i}@email.com',
            card_number=f'0000000000{i}',
            code=str(uuid.uuid4()),
        ).save()
        print(f"User successfully created! Code: {user.code}")


def init_app(app):
    connect(app.config['MONGO_URI'])
    app.cli.add_command(create_user)
    app.cli.add_command(preload_users)
