import requests_mock
from tests.conftest import MOCK_DATASERVICE


# USAGE CASE:

#  with UserContext(client,email,password) as uc:
#
#      perform actions with the created and logged user
#      condition_to_verify = Method_to_test()
#
#  exited from the context (the user has been deleted)
#  assert condition_to_verify

class UserContext:
    email = 'mock@mock.com'
    password = '42'
    mockuser = {
        'id': 42,
        'email': email,
        'firstname': 'Jhon',
        'lastname': 'Doe',
        'password': password,
        'strava_token': 'f4k&t0ken',
        'age': '22',
        'weight': '42',
        'max_hr': '42',
        'rest_hr': '42',
        'vo2max': '42'
    }

    mockruns = [{
            "title": "Example Run",
            "description": "Nice run",
            "strava_id": 42,
            "distance": 25,
            "start_date": 20181122,
            "elapsed_time": 42,
            "average_speed": 10,
            "average_heartrate": 22,
            "total_elevation_gain": 10,
            "runner_id": mockuser['id']
            },
            {
            "title": "Example Run",
            "description": "Nice run",
            "strava_id": 42,
            "distance": 25,
            "start_date": 20181122,
            "elapsed_time": 42,
            "average_speed": 10,
            "average_heartrate": 22,
            "total_elevation_gain": 10,
            "runner_id": mockuser['id']
            }]

    def __init__(self, client, requests_mock, user_json=mockuser):
        self.client = client
        self.current_user = user_json
        self.requests_mock = requests_mock

    def __enter__(self):
        self.create_user(self.client, self.request_mock, self.current_user)
        self.login(self.client, self.email, self.password)

    def __exit__(self, *args):
        self.delete_user(self.client, self.password)

    @staticmethod
    def init_mock_dataservice( requests_mock, user_json=mockuser, runs_json=mockruns ):
        requests_mock.post(MOCK_DATASERVICE + "/users", json=user_json, status_code=201)
        requests_mock.get(MOCK_DATASERVICE + "/users", json=[user_json], status_code=200)
        requests_mock.get(MOCK_DATASERVICE + "/users/" + str(user_json['id']) + "/runs", json=runs_json, status_code=200)
        requests_mock.get(MOCK_DATASERVICE + "/users/" + str(user_json['id']) + "/objectives", json=[], status_code=200)
        requests_mock.get(MOCK_DATASERVICE + "/users/" + str(user_json['id']) + "/challenges", json=[], status_code=200)

    @staticmethod
    def create_user(client, requests_mock, user_json=mockuser, runs_json=mockruns):
        UserContext.init_mock_dataservice(requests_mock, user_json, runs_json)

        response = client.post(
            '/create_user',
            data=user_json,
            follow_redirects=True
        )

        return response

    @staticmethod
    def login(client, email=mockuser['email'], password=mockuser['password']):
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
    def delete_user(client, password=mockuser['password']):
        response = client.post(
            '/delete_user',
            data=dict(
                password=password
            ),
            follow_redirects=True
        )
        return response


def create_login_user(client, user_json):
    UserContext.create_user(client, user_json)
    UserContext.login(client, user_json['email'], user_json['password'])


def delete_logged_user(client, user_json):
    UserContext.login(client, user_json['email'], user_json['password'])
    UserContext.delete_user(client, user_json['password'])

