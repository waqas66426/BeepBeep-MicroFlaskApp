from flask import request
import json

class UserDto:
    def __init__ (self, json):
        data = json.loads(request.data)
        
        self.id = data['id']
        self.email = data['email']
        self.firstname = data['firstname']
        self.lastname = data['lastname']
        self.age = data['age']
        self.weight = data['weight']
        self.max_hr = data['max_hr']
        self.rest_hr = data['rest_hr']
        self.vo2max = data['vo2max']
        self.is_active = data['is_active']
        self.is_admin = data['is_admin']
        self.is_anonymous = data['is_anonymous']

    def toJson (self):
        # return jsonify(
        #     id = self.id
        #     email = self.email
        #     firstname = self.firstname
        #     lastname = self.lastname
        #     age = self.age
        #     weight = self.weight
        #     max_hr = self.max_hr
        #     rest_hr = self.rest_hr
        #     vo2max = self.vo2max
        #     is_active = self.is_active
        #     is_admin = self.is_admin
        #     is_anonymous = self.is_anonymous
        # )

        return json.dumps(self.__dict__)
