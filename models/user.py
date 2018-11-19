from flask import request, jsonify

class User:
    def __init__ (self, json):
        data = json.loads(request.data)
        
        id = data.['id']
        email = data.['email']
        firstname = data.['firstname']
        lastname = data.['lastname']
        age = data.['age']
        weight = data.['weight']
        max_hr = data.['max_hr']
        rest_hr = data.['rest_hr']
        vo2max = data.['vo2max']
        is_active = data.['is_active']
        is_admin = data.['is_admin']
        is_anonymous = data.['is_anonymous']

    def toJson (self):
        return jsonify(
            id = self.id
            email = self.email
            firstname = self.firstname
            lastname = self.lastname
            age = self.age
            weight = self.weight
            max_hr = self.max_hr
            rest_hr = self.rest_hr
            vo2max = self.vo2max
            is_active = self.is_active
            is_admin = self.is_admin
            is_anonymous = self.is_anonymous
        )
