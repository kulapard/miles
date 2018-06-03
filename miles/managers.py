from pymodm.manager import Manager
from pymongo import DESCENDING


class UserManager(Manager):
    def get(self, card_number: int):
        return super(UserManager, self).get_queryset().get({"_id": card_number})

    def get_by_code(self, code):
        return super(UserManager, self).get_queryset().get({"code": code})


class TransactionManager(Manager):
    def get_queryset(self):
        return super(TransactionManager, self).get_queryset().order_by([("_id", DESCENDING)])

    def by_card_number(self, card_number: int, filter_: dict = None):
        query = self.get_queryset().raw({"card_number": card_number})
        if filter_:
            query = query.raw(filter_)

        return query.order_by([("date_flight", DESCENDING)])
