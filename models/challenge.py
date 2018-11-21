from flask import request
from .serializable import Serializable
import json

class Challenge(Serializable):
    def __init__(self, dict):
        if dict is not None:
            self._populate(dict)

    def toJson (self):
    # return jsonify(
    #     id = self.id
    #     runner_id = self.runner_id
    #     run_id = self.run_id
    #     latest_run_id = self.latest_run_id
    # )
        return json.dumps(self.__dict__)