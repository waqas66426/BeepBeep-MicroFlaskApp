from pyquery import PyQuery as pq
from forms import ComparisonsForm
import sys
from tests.utils import ensure_logged_in
from tests.user_context import *


def test_compare_two_run(client, db_instance, requests_mock):
    with UserContext(client, requests_mock) as uc:
        response = client.post('/comparisons', data={"runs":[1,2]})
        html = pq(response.data)
        titles = html(".title").html()
        print("@@@@@@@@@@@@@@@@@@@@@")
        print(titles)
        print(UserContext.mockruns)
        print("@@@@@@@@@@@@@@@@@@@@@")
        assert 1 == 0

    # response = client.post('/delete_user',data=dict( password=password),follow_redirects=True)