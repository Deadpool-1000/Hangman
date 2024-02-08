SIGNUP_SAMPLE_DATA = {
    'username': 'kdeadpool',
    'password': 'chimichangas'
}

SIGNUP_SAMPLE_RESPONSE = {
    'message': 'Signup Successful.'
}

SIGNUP_CONFLICT_DATA = {
    'username': 'admin',
    'password': 'different_password'
}


def test_signup(client, db_change):
    response = client.post('/signup', json=SIGNUP_SAMPLE_DATA)
    assert response.status_code == 201
    assert response.json() == SIGNUP_SAMPLE_RESPONSE


def test_signup_with_conflict(client, db_change):
    response = client.post('/signup', json=SIGNUP_CONFLICT_DATA)
    assert response.status_code == 409
