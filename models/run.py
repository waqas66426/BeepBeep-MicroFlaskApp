from flask import request
import json
from .serializable import Serializable

class Run(Serializable):

    def __init__(self, data):
        if data is not None:
            self._populate(data)