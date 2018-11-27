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
        res = pq(client.get('/').data)

        #testing set objective
        obj_distance = km2m( float ( res("#obj_dist").html() ) )
        assert obj_json['distance'] == obj_distance
        assert obj_json['user_id'] == user_id

        
        obj_json['distance'] = 100000
        requests_mock.get(MOCK_DATASERVICE + "/users/" + str(user_id) + '/objectives', json=[obj_json])
        res = pq(client.get('/').data)

        #testing changed objective
        obj_distance = km2m( float( res("#obj_dist").html() ) )
        assert obj_json['distance'] == obj_distance

        #Testing total distance in "PROGRESS" field
        total_distance = sum( run['distance'] for run in UserContext.mockruns)
        showed_tot_distance = km2m( float( res("#tot_dist").html() ) )
        assert total_distance == showed_tot_distance

        #Testing remaining distance in "PROGRESS" field
        rem_km = km2m( float( res("#rem_KM").html() ) )

        assert (rem_km >= 0.0)
        assert rem_km == (obj_distance - total_distance)


                