from flask import request

class Objective:

    def __init__(self, json):
        data = json.loads(request.data)

        distance = data['distance']
        user_id = data['user_id']