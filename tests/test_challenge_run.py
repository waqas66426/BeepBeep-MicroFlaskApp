from database import User, Run, db, Challenge
from tests.user_context import *
from forms import ChallengeForm
from tests.utils import ensure_logged_in


def _copy_run(runs, index):
    r1 = Run()
    r1.runner = runs[index].runner
    r1.strava_id = runs[index].strava_id
    r1.name = runs[index].name
    r1.average_speed = runs[index].average_speed
    r1.elapsed_time = runs[index].elapsed_time
    r1.distance = runs[index].distance
    return r1


def test_challenge_run(client, db_instance, requests_mock):

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

    # generate some runs
    runs = []
    for i in ['1', '2', '3', '4', '5']:
        # creating 5 incrementally better runs, except for the fourth one which is bad
        run = Run()

        run.runner = user
        run.strava_id = i
        run.name = "Run " + i
        if i != '4':
            run.average_speed = float(i)
            run.elapsed_time = float(i)*1000
            run.distance = 25 + float(i)
        else:
            run.average_speed = 0
            run.elapsed_time = 1
            run.distance = 1
        runs.append(run)
    #TODO jsonify the mock runs above
        
    data = {
        "id": 1,
        "run_id": 1,
        "latest_run_id": 0
    }
    r = client.post( "/users/1/challenges", json=data)
    data.update({"runner_id": 1})
    request = r.get_json()
    assert request == data


    # TODO add runs_json to create user
    UserContext.create_user(client, requests_mock, user_json=exampleuser) as uc:
        requests_mock.get(MOCK_DATASERVICE + "/user/22/challenges", json=[])

    
    