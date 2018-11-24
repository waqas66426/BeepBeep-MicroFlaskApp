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

        if prev_challenged_run_reply:
            #I did not get a 404
            prev_id = prev_challenged_run_reply[0]['id']

            # if there is already a challenge then update it
            if prev_id != runIds[0]:
                max_id_reply = requests.get(DATASERVICE + '/users/' + str(current_user.id) + '/runs/getMaxId').json()
            
                challenge_dict = {
                    "id": prev_id,
                    "runner_id": current_user.id,
                    "run_id": int (runIds[0]),
                    "latest_run_id": max_id_reply['max_id'],
                }
                reply = requests.put(DATASERVICE + '/users/' + str(current_user.id) + '/challenges/' + str(prev_id), json=challenge_dict)
        else:
            max_id_reply = requests.get(DATASERVICE + '/users/' + str(current_user.id) + '/runs/getMaxId').json()
            challenge_dict = {
                # id = 1  
                # Any better ideas??? 
                "id": 1,
                "runner_id": current_user.id,
                "run_id": int (runIds[0]),
                "latest_run_id": max_id_reply['max_id'],
                }
            reply = requests.post(DATASERVICE + '/users/' + str(current_user.id) + '/challenges', json=challenge_dict)
    else:
        return redirect("/login")

    return redirect("/")
