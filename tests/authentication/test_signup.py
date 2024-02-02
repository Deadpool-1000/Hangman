SIGNUP_SAMPLE_DATA = {
    'username': 'Fdeadpool',
    'password': 'chimichangas'
}


SIGNUP_SAMPLE_RESPONSE = {
    'message': 'Signup Successful.'
}


def test_signup(test_client, db_change):

    response = test_client.post('/signup', json=SIGNUP_SAMPLE_DATA)
    assert response.status_code == 201
    assert response.json() == SIGNUP_SAMPLE_RESPONSE
