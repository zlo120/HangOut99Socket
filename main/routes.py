from main import hangout
from flask import render_template, session, flash, redirect, url_for, request
from flask.blueprints import Blueprint
from flask_login import current_user, login_user
from flask_login.utils import login_required, login_user, logout_user
from . import app, bcrypt, db, login_manager
from .models import User, HangOutGroup, Event
from .form import Login, Register
from datetime import datetime

# Load in user
@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(ID = id).first()

mainbp = Blueprint('main', __name__)

# CODE SNIPPETS

#       This returns a list of every user in the group called "Chiller"
#  User.query.filter(User.hangoutgroup.any(Name = "Chiller")).all()

#       This returns a kust of every user in the group called "Chiller"
# HangOutGroup.query.filter_by(Name = "Chiller").first().Users

#       BOTH RETURN THE SAME THING

# Main
@mainbp.route('/', methods = ['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('event.explore'))
    
    user = None
    events = []
    groups = []
    
    if current_user.is_authenticated:
        user = User.query.filter_by(Email = current_user.Email).first()
        temp = user.hangoutgroup

        for group in temp:
            hangout = HangOutGroup.query.filter_by(Name = group.Name).first()
            groups.append(hangout)
            
    latest_event = None

    login_form = Login()

    register_form = Register()
    
    if user:
        # Query the interested_events table
        res = db.engine.execute(f"SELECT event_id FROM interested_events WHERE user_id = {user.ID};")

        plans = []
        
        for row in res:
            plans.append(Event.query.filter_by(ID = row[0]).first())

        temp = plans.copy()

        if None not in temp:

            events = []

            for plan in temp:
                if plan.DateTime != None:
                    events.append(plan)
                    plans.remove(plan)

            event_dates = []
            for event in events:
                event_dates.append( event.DateTime )  

            latest_event = None

            try:
                latest_date = min(event_dates)

                latest_event = Event.query.filter_by(DateTime = latest_date).first()

            except ValueError:
                pass

    return render_template("index.html", User = user, Event = latest_event, groups = groups, login_form = login_form)

@mainbp.route('/sockets', methods=['GET', 'POST'])
def socket():
    return render_template('socket.html')