from database import User

def test_create_user(client, db_instance):

    client.post(
        '/create_user',
        data=dict(
            email='example@test.com',
            firstname='Jhon',
            lastname='Doe',
            password='password',
            age='22',
            weight='75',
            max_hr='150',
            rest_hr='60',
            vo2max='10'
        ),
        follow_redirects=True
    )

    user = db_instance.session.query(User).filter(User.email == 'example@test.com').first()

    assert user.email == 'example@test.com'
