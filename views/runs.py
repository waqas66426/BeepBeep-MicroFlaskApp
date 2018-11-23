from flask import Blueprint, render_template
from database import db
from auth import current_user
from models.run import Run
import requests
from config import DATASERVICE
import os


runs = Blueprint('runs', __name__)

@runs.route('/runs/<int:run_id>')
def _runs(run_id):

    run_list = []
    if current_user is not None and hasattr(current_user, 'id'):
        #runs = db.session.query(Run).filter(Run.runner_id == current_user.id, Run.id == run_id).first()
        #prev_run = db.session.query(Run).filter(Run.runner_id == current_user.id, Run.id < run_id).order_by(Run.id.desc()).first()
        runs_json = requests.get(DATASERVICE + '/users/' + str(current_user.id) + '/runs').json()
        for run_json in runs_json:
            run_list.append(Run(run_json))

        runs = runs_list[run_id]
        if run_id > 0
            prev_run = runs_list[run_id -1]

    else:
        runs = None
        prev_run = None;
    return render_template("runs.html", run=runs, prev_run=prev_run)