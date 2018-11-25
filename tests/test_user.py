from database import User
from tests.user_context import UserContext, delete_logged_user, create_login_user
from random import randint

email = "mock@mock" + str(randint(0, 100)) + ".com"
password = "42"


def test_create_user(client, db_instance):
    UserContext.create_user(client, email, password)

    user = db_instance.session.query(User).filter(User.email == email).first()
    assert user is not None

    delete_logged_user(client, email, password)


def test_login_user(client, db_instance):
    UserContext.create_user(client, email, password)

    response = UserContext.login(client, email, password)
    assert response.status_code == 200

    UserContext.delete_user(client, password)


def test_badlogin_user(client, db_instance):
    UserContext.create_user(client, email, password)

    response = UserContext.login(client, email, password + "wrong")
    assert response.status_code == 401

    delete_logged_user(client, email, password)


def test_delete_user(client, db_instance):
    create_login_user(client, email, password)

    response = UserContext.delete_user(client, password)
    assert response.status_code == 200


def test_baddelete_user(client, db_instance):
    create_login_user(client, email, password)

    response = UserContext.delete_user(client, password + "wrong")
    assert response.status_code == 401

    UserContext.delete_user(client, password)