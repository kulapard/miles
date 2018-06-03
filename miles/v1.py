from flask import Blueprint
from flask import jsonify, session
from flask import request
from pymodm.errors import DoesNotExist, ValidationError

from miles.auth import login_required, requires_basic_auth
from miles.helpers import prepare_user, prepare_transaction, build_tr_filter
from miles.models import User, Transaction

ITEMS_PER_PAGE = 20  # Кол-во элементов на страницу

bp = Blueprint('v1', __name__)


@bp.route('/login', methods=['POST'])
def login():
    """Авторизует пользователя по коду и возвращает профиль.
    Код генерируется и высылается по E-mail сторонним сервисом.

    Пример запроса:
    {
      "code": 1234567890,
    }

    Пример ответа:
    {
      "card_number": 1234567890,
      "email": "taras@drapalyuk.com",
      "name": "Taras Drapalyuk"
    }
    """
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    try:
        code = request.json['code']
    except KeyError:
        return jsonify({"msg": "Invalid request"}), 400

    if not code:
        jsonify({"msg": "Invalid request"}), 400

    try:
        user = User.objects.get_by_code(code)
    except DoesNotExist:
        return jsonify({"msg": "Not found"}), 404

    session['card_number'] = user.card_number

    # Деактивируем код после авторизации пользователя
    user.code = None
    user.save()

    return jsonify(prepare_user(user)), 200


@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    """Возвращает профиль пользователя

    Пример ответа:
    {
      "card_number": 1234567890,
      "email": "taras@drapalyuk.com",
      "name": "Taras Drapalyuk"
    }
    """
    card_number = session['card_number']
    user = User.objects.get(card_number)
    return jsonify(prepare_user(user))


@bp.route('/transactions', methods=['GET'])
@login_required
def get_transactions():
    """Возвращает постранично список транзакций текущего пользователя.

    Допустимые GET-параметры:
    - page - номер страницы
    - date_flight__lte - дата полёта ОТ в ISO 8601 формате
    - date_flight__gte - дата полёта ПО в ISO 8601 формате
    - from_flight - пункт вылета
    - to_flight - пункт прилёта

    Пример ответа:
    {
      "count": 2,
      "items": [
        {
          "card_number": 1234567890,
          "date_flight": "2018-06-02T20:15:30",
          "from_flight": "Moscow",
          "miles": 1000,
          "to_flight": "Verona",
          "transaction_id": "2"
        },
        {
          "card_number": 1234567890,
          "date_flight": "2017-01-01T00:00:00",
          "from_flight": "Moscow",
          "miles": 1000,
          "to_flight": "Verona",
          "transaction_id": "1"
        },
      ],
      "limit": 20,
      "offset": 0
    }

    """
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1

    card_number = session['card_number']

    tr_query = Transaction.objects.by_card_number(
        card_number,
        filter_=build_tr_filter(request.args)
    )
    count = tr_query.count()

    per_page = ITEMS_PER_PAGE
    offset = (max(page, 1) - 1) * per_page
    limit = per_page

    tr_query = tr_query.skip(offset).limit(limit)
    transactions = tr_query.all()

    return jsonify({
        'items': list(map(prepare_transaction, transactions)),
        'count': count,
        'limit': limit,
        'offset': offset,
    })


# TODO: прикрутить нормальную авторизацию стороннего сервиса
@bp.route('/transactions', methods=['POST'])
@requires_basic_auth
def add_transaction():
    """Сохраняет новую транзакцию

    Пример JSON-запроса:
    {
        "card_number": 1234567890,
        "miles": 1000,
        "transaction_id": "1",
        "from_flight": "Moscow",
        "date_flight": "2018-05-29",
        "to_flight": "Verona"
    }
    """
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    try:
        tr = Transaction(**request.json).save()
    except ValidationError as exc:
        return jsonify({"msg": "Invalid request",
                        "params": exc.message}), 400
    return jsonify(prepare_transaction(tr)), 201


# Переопределяем хендлер, чтобы ошибка была в json-формате
@bp.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({"msg": "Too Many Requests"}), 429
