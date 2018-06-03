from pymodm import fields, MongoModel
from pymongo import DESCENDING
from pymongo.operations import IndexModel
from pymongo.read_preferences import ReadPreference

from miles.managers import UserManager, TransactionManager


class User(MongoModel):
    # Номер бонусной карты
    card_number = fields.IntegerField(primary_key=True)

    # ФИО
    name = fields.CharField(required=True)

    # E-mail
    email = fields.EmailField(required=True)

    # Код для авторизации пользователя (высылается на E-mail)
    code = fields.CharField(blank=True)

    objects = UserManager()


class Transaction(MongoModel):
    # Номер транзакции
    # В общем случе не уникален, так как это "код транзакции в другой системе"
    transaction_id = fields.CharField(required=True)

    # Номер бонусной карты того, кто летел
    card_number = fields.IntegerField(required=True)

    # Сколько начислено бонусных единиц (миль)
    miles = fields.IntegerField(required=True)

    # Дата полёта (храним и возвращаем в UTC)
    date_flight = fields.DateTimeField(required=True)

    # Откуда
    from_flight = fields.CharField(required=True)

    # Куда
    to_flight = fields.CharField(required=True)

    objects = TransactionManager()

    class Meta:
        # Для скорейшей выборки данных настраиваем индексы
        indexes = [
            IndexModel([
                ('card_number', DESCENDING),
                ('date_flight', DESCENDING)
            ]),
        ]
        # Для снижения нагрузки на PRIMARY ноду читаем из SECONDARY
        read_preference = ReadPreference.SECONDARY
