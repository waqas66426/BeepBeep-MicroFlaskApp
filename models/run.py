from flask import request
import json

class Run:

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.strava_id = data['strava_id']
        self.distance = data['distance']
        self.start_date = data['start_date']
        self.elapsed_time = data['elapsed_time']
        self.average_speed = data['average_speed']
        self.average_heartrate = data['average_heartrate']
        self.total_elevation_gain = data['total_elevation_gain']
        self.runner_id = data['runner_id']

    def toJson (self):
        # return jsonify(
        #     id = self.id
        #     title = self.title
        #     strava_id = self.strava_id
        #     distance = self.distance
        #     start_date = start_date
        #     elapsed_time = self.elapsed_time
        #     average_speed = self.average_speed
        #     average_heartrate = self.average_heartrate
        #     total_elevation_gain = self.total_elevation_gain
        #     runner_id = self.runner_id
        # )

        return json.dumps(self.__dict__)