from database import User
from tests.user_context import UserContext, delete_logged_user, create_login_user
from random import randint

email = "mock@mock" + str(randint(0, 100)) + ".com"
password = "42"


def test_create_user(client, db_instance):
    UserContext.create_user(client, email, password)

    user = db_instance.session.query(User).filter(User.email == email).first()
    delete_logged_user(client, email, password)

    assert user is not None


def test_login_user(client, db_instance):
    UserContext.create_user(client, email, password)

    response = UserContext.login(client, email, password)
    UserContext.delete_user(client, password)

    assert response.status_code == 200


def test_badlogin_user(client, db_instance):
    UserContext.create_user(client, email, password)

    response = UserContext.login(client, email, password + "wrong")
    delete_logged_user(client, email, password)

    assert response.status_code == 401


def test_delete_user(client, db_instance):
    create_login_user(client, email, password)

    response = UserContext.delete_user(client, password)
    assert response.status_code == 200


def test_baddelete_user(client, db_instance):
    create_login_user(client, email, password)

    response = UserContext.delete_user(client, password + "wrong")
    UserContext.delete_user(client, password)

    assert response.status_code == 401