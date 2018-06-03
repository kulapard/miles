def test_profile(client, auth):
    res = client.get('/profile')
    assert res.status_code == 401

    print(auth.login())
    res = client.get('/profile')
    assert res.status_code == 200


def test_transactions(client, auth):
    res = client.get('/transactions')
    assert res.status_code == 401

    print(auth.login())
    res = client.get('/transactions')
    assert res.status_code == 200
