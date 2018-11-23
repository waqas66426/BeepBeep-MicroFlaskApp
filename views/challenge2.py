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
        # prev_challenged_run = db.session.query(Challenge).filter(Challenge.runner_id == current_user.id).first()

        # TODO add .FIRST() see above
        prev_challenged_run = requests.get(DATASERVICE + '/users/' + str(current_user.id) + '/challenges').json()

        print("****************************")
        print("****************************")
        print(prev_challenged_run)
        print("****************************")
        print("****************************")

        # found a previosly challenged run, gotta make it unchallenged and then challenge the next one
        if prev_challenged_run:
            db.session.delete(prev_challenged_run)
            if prev_challenged_run.run_id != int(runIds[0]):
                # I'm not unchallenging a run, but challenging a new one
                #new_challenge = db.session.query(Run).filter(Run.runner_id == current_user.id, Run.id == runIds[0]).first()
                
                # TODO
                # new_challenge = requests.post(DATASERVICE + '/users' + str(current_user.id) + '/challenges', json=new_user.to_json())
                
                if new_challenge is not None:
                    # TODO
                    # complete dictionary
                    challenge_dict = {
                        "id": new_challenge
                        "run_id": runIds[0]
                        "runner": current_user
                        "runner_id": current_user.id

                    }
                    # ???
                    latest_id = db.session.query(func.max(Run.id)).scalar()
                    challenge.latest_run_id = latest_id
                    db.session.add(challenge)
            db.session.commit()

        else:  # just challenge the new one

            # new_challenge = db.session.query(Run).filter(Run.runner_id == current_user.id, Run.id == runIds[0]).first()

            # TODO
            # new_challenge = requests.post(DATASERVICE + '/users' + str(current_user.id) + '/challenges', json=new_user.to_json())

            if new_challenge is not None:
                # TODO
                # complete dictionary
                challenge_dict = {
                    "id": new_challenge
                    "run_id": runIds[0]
                    "runner": current_user
                    "runner_id": current_user.id

                }
                # ???
                latest_id = db.session.query(func.max(Run.id)).scalar()
                challenge.latest_run_id = latest_id
                db.session.add(challenge)

            db.session.commit()
    else:
        return redirect("/login")

    return redirect("/")
