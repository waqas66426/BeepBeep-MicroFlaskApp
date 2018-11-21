from flask import request
import json
from .serializable import Serializable

class Objective(Serializable):
    def __init__(self, dict):
        if dict is not None:
            self._populate(dict)
    
    def toJson (self):
        # return jsonify(
        #     objective_id = self.objective_id
        #     distance = self.distance
        #     user_id = self.user_id
        # )

        return json.dumps(self.__dict__)