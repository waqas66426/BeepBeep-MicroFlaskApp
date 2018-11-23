from flask import Blueprint, render_template, request, redirect
from stravalib import Client
from database import db, User
from auth import current_user
from forms import ObjectiveForm
from views.auth import *
from views.util import *
from models.objective import Objective
import requests
import os


objective = Blueprint('objective', __name__)

DATASERVICE = os.environ['DATA_SERVICE']


@objective.route('/objective', methods=['GET', 'POST'])
def set_objective():
    form = ObjectiveForm()

    if form.validate_on_submit():
        existing_objective = None
        objective_distance = km2m(form.data['distance'])
        q = db.session.query(User).filter(User.email == current_user.email)
        user = q.first()

        #existing_objective = db.session.query(Objectives).filter(Objectives.user == user).first()
        obj_json = requests.get(DATASERVICE + '/users/' + str(current_user.id) + '/objectives').json()

        if obj_json:
            existing_objective = Objective(obj_json[0])

        if existing_objective is None:
            #_setObjective(user, objective_distance)
            requests.post(DATASERVICE + '/users/' + str(current_user.id) + '/objectives', json = { 'distance' : objective_distance})

        else:
            #existing_objective.set_distance(objective_distance)
            existing_objective.distance = objective_distance
            r = requests.put(DATASERVICE + '/users/' + str(current_user.id) + '/objectives/' + str(existing_objective.id), json = existing_objective.toJson())


        #db.session.commit()
        return redirect("/")

    return render_template('set_objective.html', form = form)