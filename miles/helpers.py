from pymodm.vendor import parse_datetime


def prepare_user(user) -> dict:
    """Подготавливаем объект User для ответа"""
    return {
        'name': user.name,
        'email': user.email,
        'card_number': user.card_number,
    }


def prepare_transaction(tr) -> dict:
    """Подготавливаем объект Transaction для ответа"""
    return {
        'transaction_id': tr.transaction_id,
        'card_number': tr.card_number,
        'miles': tr.miles,
        'from_flight': tr.from_flight,
        'to_flight': tr.to_flight,
        'date_flight': tr.date_flight.isoformat(),
    }


def build_tr_filter(args: dict) -> dict:
    """Возвращает словарь для фильтрации транзакций согласно заданным аргументам"""
    filter_ = {}

    # По совпадению пункта вылета/прилёта
    for f_name in ('from_flight', 'to_flight'):
        if f_name in args:
            filter_[f_name] = args[f_name]

    # По диапазону дат полёта
    dt_flt_filter = {}
    if 'date_flight__lte' in args:
        dt_flt_filter['$lte'] = parse_datetime(args['date_flight__lte'])

    if 'date_flight__gte' in args:
        dt_flt_filter['$gte'] = parse_datetime(args['date_flight__gte'])

    if dt_flt_filter:
        filter_['date_flight'] = dt_flt_filter

    return filter_
