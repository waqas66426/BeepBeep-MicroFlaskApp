from flask import request

class Run:

    def __init__(self, json):

        data = json.loads(request.data)

        id = data['id']
        name = data['name']
        strava_id = data['strava_id']
        distance = data['distance']
        start_date = data['start_date']
        elapsed_time = data['elapsed_time']
        average_speed = data['average_speed']
        average_heartrate = data['average_heartrate']
        total_elevation_gain = data['total_elevation_gain']
        runner_id = data['runner_id']