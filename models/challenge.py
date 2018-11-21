from flask import request
import json

class Challenge:
    def __init__ (self, json):
        data = json.loads(request.data)

        id = data['id'] 
        runner_id = data['runner_id']
        run_id = data['run_id']
        latest_run_id = data['latest_run_id']
    

    def toJson (self):
        # return jsonify(
        #     id = self.id
        #     runner_id = self.runner_id
        #     run_id = self.run_id
        #     latest_run_id = self.latest_run_id
        # )

        return json.dumps(self.__dict__)