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
    run = None
    prev_run = None
    if current_user is not None and hasattr(current_user, 'id'):
        #runs = db.session.query(Run).filter(Run.runner_id == current_user.id, Run.id == run_id).first()
        #prev_run = db.session.query(Run).filter(Run.runner_id == current_user.id, Run.id < run_id).order_by(Run.id.desc()).first()
        runs_json = requests.get(DATASERVICE + '/users/' + str(current_user.id) + '/runs').json()
    
        for run_json in runs_json:
            run_list.append(Run(run_json))
            if run_list[-1].id == run_id:
                run = run_list[-1]
                
                if len(run_list) == 1:
                    prev_run = run
                else:
                    prev_run = run_list[-2]

    return render_template("runs.html", run=run, prev_run=prev_run)