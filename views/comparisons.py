from flask import Blueprint, redirect, render_template, request
from database import db, User, _delete_user
from auth import admin_required
from forms import UserForm, ComparisonsForm
from flask_login import current_user, logout_user
from models.run import Run
from config import DATASERVICE
import requests
import os

comparisons = Blueprint('comparisons', __name__)

@comparisons.route("/comparisons", methods=['POST'])
def post_comparisons():

    form = ComparisonsForm()

    runIds = form.data['runs']

    if runIds is None or len(runIds) <= 1:
        return redirect('/?comparisonError=Please select at least 2 runs.')

    if current_user is not None and hasattr(current_user, 'id'):
        #runsId = list(map(int, runIds))
        #runs = db.session.query(Run).filter(Run.runner_id == current_user.id, Run.id.in_(runIds))
        runs_json = requests.get(DATASERVICE + '/users/' + str(current_user.id) + '/runs').json()
        runs = []
    
        for tmp_run in runs_json:
            if (str (tmp_run['id'])) in runIds:
                runs.append(tmp_run)
    else:
        runs = []

    # for r in runs:
    #     r['average_speed'] = "{:.2f}".format(r.average_speed * 3.6)
    #     r['elapsed_time'] = "{:.0f}".format(r.elapsed_time // 60) + "." + "{:.0f}".format(r.elapsed_time % 60)


    return render_template('comparisons.html', runs=runs)
