from flask import request
import json

class Objective:

    def __init__(self, json):
        data = json.loads(request.data)

        objective_id = data['objective_id']
        distance = data['distance']
        user_id = data['user_id']
    
    def toJson (self):
        # return jsonify(
        #     objective_id = self.objective_id
        #     distance = self.distance
        #     user_id = self.user_id
        # )

        return json.dumps(self.__dict__)
    
