from database import User
from tests.user_context import *
from views.util import km2m
from pyquery import PyQuery as pq
import re

def test_objective(client, db_instance, requests_mock):
    
    with UserContext(client, requests_mock) as _ :
        user_id = UserContext.mockuser['id']
        
        #fake objective
        obj_json = {
            'distance' : 100,
            'user_id' : user_id
            }
        
        requests_mock.get(MOCK_DATASERVICE + "/users/" + str(user_id) + '/objectives', json=[obj_json])
        html = pq(client.get('/').data).text()
        showed_distance = re.search( 'Distance objective: (.*) km', html).group(1)
        
        assert obj_json['distance'] == km2m(float(showed_distance))
        assert obj_json['user_id'] == user_id

        #change objective
        obj_json['distance'] = 10

        requests_mock.get(MOCK_DATASERVICE + "/users/" + str(user_id) + '/objectives', json=[obj_json])
        html = pq(client.get('/').data).text()
        showed_distance = re.search( 'Distance objective: (.*) km', html).group(1)
        
        assert obj_json['distance'] == km2m(float(showed_distance))