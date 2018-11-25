from flask import Blueprint, render_template, redirect, request
from flask_login import (current_user, login_user, logout_user,
                         login_required)
from stravalib import Client

from database import db, User
from forms import LoginForm
from background import *
import requests
from config import DATASERVICE

auth = Blueprint('auth', __name__)


@auth.route('/strava_auth')
@login_required
def _strava_auth():
    code = request.args.get('code')
    client = Client()
    xc = client.exchange_code_for_token
    access_token = xc(client_id=auth.app.config['STRAVA_CLIENT_ID'],
                      client_secret=auth.app.config['STRAVA_CLIENT_SECRET'],
                      code=code)
    current_user.strava_token = access_token

    user = requests.get(DATASERVICE + '/users/' + str(current_user.id)).json()
    user['strava_token'] = access_token
    requests.put(DATASERVICE + '/users/' + str(current_user.id), json=user).json()


    db.session.add(current_user)
    db.session.commit()
    # fetch_runs(current_user)
    return redirect('/')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = False
    status_code = 200
    if form.validate_on_submit():
        email, password = form.data['email'], form.data['password']
        q = db.session.query(User).filter(User.email == email)
        user = q.first()
        print(email + password)
        if user is not None and user.authenticate(password):
            login_user(user)
            return redirect('/')
        else:
            error = True
            status_code = 401

    return render_template('login.html', form=form, error=error), status_code


@auth.route("/logout")
def logout():
    logout_user()
    return redirect('/')
