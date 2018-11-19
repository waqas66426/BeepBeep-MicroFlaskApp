from flask import request

class Challenge:
    def __init__ (self, json):
        data = json.loads(request.data)

        id = data['id'] 
        runner_id = data['runner_id']
        run_id = data['run_id']
        latest_run_id = data['latest_run_id']