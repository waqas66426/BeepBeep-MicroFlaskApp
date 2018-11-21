from flask import request
import json
from .serializable import Serializable

class UserDto(Serializable):
    def __init__ (self, dict):
        if dict is not None:
            self._populate(dict)

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
