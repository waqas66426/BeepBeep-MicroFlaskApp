from flask import request
import json
from .serializable import Serializable

class Run(Serializable):

    def __init__(self, data):
        if data is not None:
                self._populate(data)
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
