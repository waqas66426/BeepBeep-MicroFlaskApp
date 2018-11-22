from flask import Blueprint, redirect, render_template, request, jsonify, g
from database import db, _delete_user
from auth import admin_required
from forms import UserForm, DeleteForm
from flask_login import current_user, logout_user

from models.user import UserDto
from database import User
from models.run import Run
import requests
import os
import json
from config import DATASERVICE


users = Blueprint('users', __name__)


@users.route('/users')
def _users():
    users = requests.get(DATASERVICE + '/users').json()
    return render_template("users.html", users=users)


@users.route('/create_user', methods=['POST', 'GET'])
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        new_user = User()        
        form.populate_obj(new_user)
        new_user.set_password(form.password.data)

        print(new_user.to_json())

        # response = requests.post(DATASERVICE + '/users', json=new_user.to_json())

        # new_user.id = response['id']

        # print(new_user.to_json())

        # db.session.add(new_user)
        # db.session.commit()
        # print(response)

        return redirect('/users')

    return render_template('create_user.html', form=form)


@users.route("/delete_user", methods=['DELETE'])
def delete_user():
    form = DeleteForm()
    try:
        email = current_user.email
    except AttributeError:
        return redirect('/login')

    if form.validate_on_submit():
        # verify user password
        password = form.data['password']

        #q = db.session.query(User).filter(User.id == current_user.id)
        #user = q.first()
        user = requests.delete(DATASERVICE + '/users/' + str(current_user.id))

        if user is not None and user.authenticate(password):
            logout_user()
            # delete the user and all his data
            _delete_user(user)
            return redirect('/users')

    return render_template('delete_user.html', form=form, user_email=email)
