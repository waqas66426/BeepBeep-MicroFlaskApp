from flask import request
from .serializable import Serializable

class Objective(Serializable):

    def __init__(self, dict):
        if dict is not None:
            self._populate(dict)