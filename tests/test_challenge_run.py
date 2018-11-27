from tests.user_context import *

from pyquery import PyQuery as pq


# def _copy_run(runs, index):
#     r1 = Run()
#     r1.runner = runs[index].runner
#     r1.strava_id = runs[index].strava_id
#     r1.name = runs[index].name
#     r1.average_speed = runs[index].average_speed
#     r1.elapsed_time = runs[index].elapsed_time
#     r1.distance = runs[index].distance
#     return r1


def test_challenge_run(client, db_instance, requests_mock):

    # generate some runs
    runs = []
    for i in ['1', '2', '3', '4', '5']:
        # creating 5 incrementally better runs, except for the fourth one which is bad
        run = {
            "id": i,
            "title": "Example Run"+str(i),
            "description": "Nice run "+str(i),
            "strava_id": 42,
            "runner_id": 42,
            "start_date": "2018112"+str(i),
            "average_heartrate": 22,
            "total_elevation_gain": 10,
        }
        d = {}
        if i != '4':
            d.update({
                "average_speed": float(i),
                "elapsed_time": float(i)*1000,
                "distance": 25 + float(i),
            })
        else:
            d.update({
                "average_speed": 0,
                "elapsed_time": 1,
                "distance": 1,
            })
        run.update(d)
        runs.append(run)


    with UserContext(client, requests_mock, runs_json=runs) as uc:
        data = {
            "id": 1,
            "run_id": 1,
            "runner_id": 42,
            "latest_run_id": 5
        }
        requests_mock.get(MOCK_DATASERVICE + "/users/42/challenges", json=[data], status_code=200)
        requests_mock.get(MOCK_DATASERVICE + "/users/42/runs/getMaxId", json={"max_id": 5}, status_code=200)

        res = client.post("/challenge", data={"run":[1]}, follow_redirects=True)
        
        html = pq(res.data)
        
        v = [i.attr("style") for i in html.items('.run')]
        
        assert v[data["run_id"]-1] == "color:yellow"

        #check the view converting the distance to km
        # assert objective_view == objective_distance



    
    