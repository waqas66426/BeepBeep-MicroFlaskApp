from flask import Blueprint, redirect, render_template, request
from database import db, _delete_user
from sqlalchemy import func
from auth import admin_required
from forms import UserForm, ChallengeForm
from flask_login import current_user, logout_user

from models.user import UserDto
from models.run import Run
from models.challenge import Challenge
from database import User
import requests
import os
import json
from config import DATASERVICE


challenge = Blueprint('challenge', __name__)


@challenge.route("/challenge", methods=['POST'])
def post_challenge():

    form = ChallengeForm()
    runIds = form.data['runs']

    if runIds is None or len(runIds) != 1:
        return redirect('/?challengeError=Please select exactly one run to challenge')

    if current_user is not None and hasattr(current_user, 'id'):

        prev_challenged_run_reply = requests.get(DATASERVICE + '/users/' + str(current_user.id) + '/challenges').json()
        
        print(":::::::::::::::::::::")
        print(prev_challenged_run_reply)
        print(runIds)
        print(":::::::::::::::::::::")
        
        # prev_challenged_run = -1

        if prev_challenged_run_reply:
            #I did not get a 404
            prev_challenged_run = prev_challenged_run_reply[0]['id']
        
            print(":::::::::::::::::::::")
            print(prev_challenged_run_reply)
            print(prev_challenged_run)
            print(runIds)
            print(":::::::::::::::::::::")
            # if there was a challenge and it was not the same as before
            if prev_challenged_run != runIds[0]:
                # I delete the previous challenge
                resp = requests.delete(DATASERVICE + '/users/' + str(current_user.id) + '/challenges/' + str(runIds[0]))
                # I retreive the latest fetched run, so I can fetch the following ones
                max_id_reply = requests.get(DATASERVICE + '/users/' + str(current_user.id) + '/runs/getMaxId').json()
            
                challenge_dict = {
                    "id": 1,
                    "runner_id": current_user.id,
                    "run_id": int (runIds[0]),
                    "latest_run_id": max_id_reply['max_id'],
                }
                reply = requests.post(DATASERVICE + '/users/' + str(current_user.id) + '/challenges', json=challenge_dict)
                print("*****************************")
                print(resp)
                print(json.dumps(challenge_dict))
                print(max_id_reply)
                print(reply)
                print("*****************************")
        else:
            max_id_reply = requests.get(DATASERVICE + '/users/' + str(current_user.id) + '/runs/getMaxId').json()
            challenge_dict = {
                "id": 1,
                "runner_id": current_user.id,
                "run_id": int (runIds[0]),
                "latest_run_id": max_id_reply['max_id'],
                }
            reply = requests.post(DATASERVICE + '/users/' + str(current_user.id) + '/challenges', json=challenge_dict))
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print(json.dumps(challenge_dict))
            print(max_id_reply)
            print(reply)
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    else:
        return redirect("/login")

    return redirect("/")
