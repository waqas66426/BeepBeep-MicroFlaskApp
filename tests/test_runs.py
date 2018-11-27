import random
from tests.user_context import *
from pyquery import PyQuery as pq

def test_single_run(client,db_instance, requests_mock):
	with UserContext(client,requests_mock) as uc:
		response = client.get("/runs/1")
		assert response.status_code == 200


def test_home_runs(client,db_instance, requests_mock):
	with UserContext(client, requests_mock) as uc:

		response=client.get("/")
		html = pq(response.data)

		run_list = []
		for i in html.items('.run'):
			run_list.append(i.text())

		assert run_list[0] == UserContext.mockruns[0]['title']
		assert run_list[1] == UserContext.mockruns[1]['title']


def test_single_run_view(client,db_instance, requests_mock):
	with UserContext(client,requests_mock) as uc:
		response = client.get("/runs/1")

		html = pq(response.data)
		run_speed=int(html("#run_speed").text())
		assert run_speed == UserContext.mockruns[0]['average_speed']


def test_bad_singlerun(client,db_instance, requests_mock):
	with UserContext(client,requests_mock) as uc:
		response = client.get("/runs/100")

		html = pq(response.data)
		warning_div = html(".text-danger")

		assert warning_div is not None
