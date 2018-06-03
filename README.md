Miles
=====

API для работы с накопленными милями пользователя


Установка и запуск
------------------
```
git clone https://github.com/kulapard/miles
cd miles
docker-compose up app
```

Тестирование
------------
```
docker-compose up test
``` 

Предустановка в базе 10 пользователей
----

```
docker-compose run app flask preload-users
```

Пример использования
---
Авторизация:
```
curl -X "POST" "http://127.0.0.1:5000/login" \
     -H 'Content-Type: application/json; charset=utf-8' \
     -d $'{
  "code": "<code>"
}'
```

Получение профиля пользователя:
```
curl "http://127.0.0.1:5000/profile" \
     -H 'Cookie: session=<session_id>'
```

Получение списка транзакций по заданному фильтру:
```
curl "http://127.0.0.1:5000/transactions?page=1&date_flight__lte=2018-06-01&date_flight__gte=2018-01-01&from_flight=Moscow&to_flight=Verona" \
     -H 'Cookie: session=<session_id>'
```

Добавление транзакции:
```
curl -X "POST" "http://127.0.0.1:5000/transactions" \
     -H 'Content-Type: application/json; charset=utf-8' \
     -u 'admin:admin' \
     -d $'{
  "card_number": "00000000",
  "miles": 1000,
  "transaction_id": "1234",
  "from_flight": "Moscow",
  "date_flight": "2018-06-04",
  "to_flight": "Verona"
}'
```
TODO
----
- дописать тесты под все методы API
- прикрутить нормальную авторизацию сторонней системы