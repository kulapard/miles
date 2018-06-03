import datetime

from miles.helpers import build_tr_filter


def test_builder():
    # Нормальные данные
    data = {
        'from_flight': 'qwer',
        'to_flight': 'asdf',
        'date_flight__lte': '2017-05-6',
        'date_flight__gte': '2017-06-1',
    }
    exp_date_flight = {
        '$lte': datetime.datetime(2017, 5, 6, 0, 0),
        '$gte': datetime.datetime(2017, 6, 1, 0, 0),
    }
    res = build_tr_filter(data)
    assert len(res) == 3
    assert res['from_flight'] == data['from_flight']
    assert res['to_flight'] == data['to_flight']
    assert res['date_flight'] == exp_date_flight

    # Невалидные данные
    data = {
        'date_flight__lte': '2017-05-asdasdasd',
        'date_flight__gte': '2017-06-asddsadasd',
    }
    exp_date_flight = {
        '$lte': None,
        '$gte': None,
    }
    res = build_tr_filter(data)
    assert len(res) == 1
    assert res['date_flight'] == exp_date_flight

