
class UserContext():

    def __init__(self, client, email, password):
        self.client = client
        self.email = email
        self.password = password

    def __enter__(self):
        self.create_user(self.client, self.email, self.password)
        self.login(self.client, self.email, self.password)

    def __exit__(self, *args):
        self.delete_user(self.client, self.password)

    @staticmethod
    def create_user(client, email, password):
        response = client.post(
            '/create_user',
            data=dict(
                email=email,
                firstname='Jhon',
                lastname='Doe',
                password=password,
                age='22',
                weight='42',
                max_hr='42',
                rest_hr='42',
                vo2max='42'
            ),
            follow_redirects=True
        )

        return response

    @staticmethod
    def login(client, email, password):
        response = client.post(
            '/login',
            data=dict(
                email=email,
                password=password
            ),
            follow_redirects=True
        )
        return response

    @staticmethod
    def delete_user(client, password):
        response = client.post(
            '/delete_user',
            data=dict(
                password=password
            ),
            follow_redirects=True
        )
        return response


def create_login_user(client, email, password):
    UserContext.create_user(client, email, password)
    UserContext.login(client, email, password)


def delete_logged_user(client, email, password):
    UserContext.login(client, email, password)
    UserContext.delete_user(client, password)

