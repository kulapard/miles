import os
import uuid

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

__author__ = 'Taras Drapalyuk <taras@drapalyuk.com>'
__date__ = '25.05.2018'


def create_app(test_config=None):
    """Создаёт и конфигурирует Flask-приложение"""
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=os.getenv('APP_SECRET_KEY', str(uuid.uuid4())),
        MONGO_URI=os.getenv('APP_MONGO_URI'),
        RATELIMIT_STORAGE_URL=os.getenv('APP_REDIS_URI'),

        # Для авторизации стороннего сервиса
        LOGIN=os.getenv('APP_LOGIN'),
        PASSWORD=os.getenv('APP_PASSWORD'),
    )

    if test_config is not None:
        app.config.update(test_config)

    app.secret_key = app.config['SECRET_KEY']
    limiter = Limiter(
        app,
        key_func=get_remote_address,
    )

    # Важно: импорт моделей должен идти после вызова connect (особенность pymodm)
    # http://pymodm.readthedocs.io/en/latest/api/index.html#module-pymodm.connection
    from miles import db
    db.init_app(app)

    from miles import v1
    # Чтобы трудно было подобрать код, ставим лимит на запросы
    limiter.limit("10/hour")(v1.login)

    app.register_blueprint(v1.bp)

    return app
