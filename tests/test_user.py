from database import User
from tests.user_context import *
from random import randint

email = "mock@example.com"
password = "7"

exampleuser = {
            'id': 22,
            'email': email,
            'firstname': 'Mario',
            'lastname': 'Rossi',
            'password': password,
            'strava_token' : 'f4k&t0ken',
            'age': '7',
            'weight': '22',
            'max_hr': '22',
            'rest_hr': '22',
            'vo2max': '7'
        }


def test_create_user(client, db_instance, requests_mock ):
    UserContext.create_user(client, requests_mock, user_json=exampleuser)

    user = db_instance.session.query(User).filter(User.email == email).first()
    assert user is not None


def test_login_user(client, db_instance, requests_mock):
    UserContext.create_user(client, requests_mock)
    response = UserContext.login(client)

    assert response.status_code == 200


def tst_badlogin_user(client, db_instance):
    UserContext.create_user(client, email, password)

    response = UserContext.login(client, email, password + "wrong")
    delete_logged_user(client, email, password)

    assert response.status_code == 401


def tst_delete_user(client, db_instance):
    create_login_user(client, email, password)

    response = UserContext.delete_user(client, password)
    assert response.status_code == 200


def tst_baddelete_user(client, db_instance):
    create_login_user(client, email, password)

    response = UserContext.delete_user(client, password + "wrong")
    UserContext.delete_user(client, password)

    assert response.status_code == 401