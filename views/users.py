from flask import Blueprint, redirect, render_template, request, jsonify
from database import db, _delete_user
from auth import admin_required
from forms import UserForm, DeleteForm
from flask_login import current_user, logout_user

from models.user import User
from models.user_no_id import UserNoId
from models.run import Run
import requests, os, json



users = Blueprint('users', __name__)
DATASERVICE = os.environ['DATA_SERVICE']


@users.route('/users')
def _users():
    users = requests.get(DATASERVICE + '/users').json()
    return render_template("users.html", users=users)


@users.route('/create_user', methods=['POST'])
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        data = json.loads(request.data)
        new_user = UserNoId(data)
        #form.populate_obj(new_user)

        #TODO  
        #new_user.set_password(form.password.data) #pw should be hashed with some salt
        
        #db.session.add(new_user)
        #db.session.commit()
        new_user_json = new_user.toJson()
        requests.post(DATASERVICE + '/users' , json=new_user_json)

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
        #verify user password
        password = form.data['password']

        #q = db.session.query(User).filter(User.id == current_user.id)
        #user = q.first()
        user = requests.delete(DATASERVICE + '/users/' + str(current_user.id))

        if user is not None and user.authenticate(password):
            logout_user()
            #delete the user and all his data
            _delete_user(user)
            return redirect('/users')

    return render_template('delete_user.html', form=form, user_email=email)
