from flask import Blueprint, render_template, request, redirect, g
from flask_login import current_user
from stravalib import Client
from database import db

from models.user import UserDto
from models.objective import Objective
from models.challenge import Challenge
from models.run import Run

from auth import current_user
from forms import ObjectiveForm
from views.auth import *
from views.util import *
import requests
import json
from config import DATASERVICE

home = Blueprint('home', __name__)


def _strava_auth_url(config):
    client = Client()
    client_id = config['STRAVA_CLIENT_ID']
    redirect = 'http://127.0.0.1:5000/strava_auth'
    url = client.authorization_url(client_id=client_id,
                                   redirect_uri=redirect)
    return url


@home.route('/')
def index():
    if request.args.get('comparisonError') is None:
        comparisonError = ""
    else:
        comparisonError = request.args.get('comparisonError')

    if request.args.get('challengeError') is None:
        challengeError = ""
    else:
        challengeError = request.args.get('challengeError')

    avgSpeed = 0
    objective_distance = 0
    tot_distance = 0
    elapsed_time = 0
    remaining_KM = 0
    minutes = 0
    sec = 0

    if current_user is not None and hasattr(current_user, 'id'):
        runListDict = requests.get(
            DATASERVICE + '/users/' + str(current_user.id) + '/runs').json()

        runs = []
        for r in runListDict:
            runs.append(Run(r))

        if len(runs) > 0:
            for r in runs:
                avgSpeed += r.average_speed
                tot_distance += r.distance
                elapsed_time += r.elapsed_time
            avgSpeed /= len(runs)

            minutes, sec = sec2minsec(elapsed_time)

        # objective = None#db.session.query(Objectives).filter(Objectives.user_id == current_user.id).first()
        objective = requests.get(
            DATASERVICE + '/users/' + str(current_user.id) + '/objectives').json()
        if objective:
            objective_distance = objective[0]['distance']

        # handling challenges
        # colored lists for runs to be challenged
        yellow = []
        red = []
        green = []
        orange = []
        # fetch the run selected for the challenge
        challenged_run_reply = requests.get(
            DATASERVICE + '/users/' + str(current_user.id) + '/challenges').json()
        if challenged_run_reply:
            challenged_run = challenged_run_reply[0]
            # the challenged run is print in yellow
            yellow.append(challenged_run['run_id'])
            # fetching runs stored only after the selection of the challenged run
            #after_challenge_run = []
            #db.session.query(Run).filter(current_user.id == Run.runner_id, Run.id > challenged_run.latest_run_id).all()

            ch_run = last_run = requests.get(
                DATASERVICE + '/users/' + str(current_user.id) + '/runs/' + str(challenged_run['run_id'])).json()

            last_run_id = requests.get(
                DATASERVICE + '/users/' + str(current_user.id) + '/runs/getMaxId').json()['max_id']

            last_run = requests.get(
                DATASERVICE + '/users/' + str(current_user.id) + '/runs/' + str(last_run_id)).json()
            print("@@@@@@@@@@@@@@@@@@@@@")
            print(challenged_run)
            print(ch_run)
            print(last_run)
            print("@@@@@@@@@@@@@@@@@@@@@")

            last_run_pace = last_run['distance'] / last_run['elapsed_time']
            ch_run_pace = ch_run['distance'] / ch_run['elapsed_time']

            # fills appropriate lists depending on run performances
            if last_run_pace > ch_run_pace:
                green.append(last_run['id'])
            elif last_run_pace <= ch_run_pace:
                red.append(last_run['id'])
            else:
                orange.append(last_run['id'])

    else:
        return redirect("/login")

    strava_auth_url = _strava_auth_url(home.app.config)

    if objective_distance - tot_distance > 0:
        remaining_KM = objective_distance - tot_distance
        percentage = (tot_distance/objective_distance)*100
    else:
        percentage = 100

    return render_template(
        "index.html",
        runs=runs,
        strava_auth_url=strava_auth_url,
        avgSpeed=mh2kmh(avgSpeed),
        minutes=minutes,
        sec=sec,
        comparisonError=comparisonError,
        challengeError=challengeError,
        objective_distance=m2km(objective_distance),
        tot_distance=m2km(tot_distance),
        remaining_KM=m2km(remaining_KM),
        percentage=percentage,
        challenge_orange=orange,
        challenge_red=red,
        challenge_green=green,
        challenged_run=yellow
    )
