from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, FileField, SelectField, PasswordField
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import *
from datetime import datetime

from .models import Event
from .utils import user_loader

# choices = [(data, display)]

def groups(current_user):
    groups = []

    for group in current_user.hangoutgroup:
        groups.append( ( (group.Name), group.Name))

    return groups

def createEditForm(current_user, event):
    class EditEvent(FlaskForm):
        title = StringField("Title *", validators=[InputRequired()], render_kw={"placeholder": "Name of the event", "value" : event.Name})
        description = TextAreaField("Description *", validators=[InputRequired()], render_kw={"rows":"10","placeholder": "Description of the event"})
        date = DateField("Date", validators=[Optional()])
        time = TimeField("Time", validators=[Optional()])
        location = StringField("Location address", validators=[Optional()], render_kw={"placeholder": "Location address", "value" : event.Location})
        group = SelectField("Hangout Group", choices=groups(current_user))
        submit = SubmitField("Submit")

    return EditEvent() 

def createEventForm(current_user):
    class CreateEvent(FlaskForm):
        title = StringField("Title *", validators=[InputRequired()], render_kw={"placeholder": "Name of the event"})
        description = TextAreaField("Description *", validators=[InputRequired()], render_kw={"rows":"10","placeholder": "Description of the event"})
        date = DateField("Date", validators=[Optional()])
        time = TimeField("Time", validators=[Optional()])
        group = SelectField("Hangout Group", choices=groups(current_user) )
        location = StringField("Location address", validators=[Optional()], render_kw={"placeholder": "Location address"})
        submit = SubmitField("Submit")

    return CreateEvent()

class Register(FlaskForm):
    profile = StringField("Profile", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email()], render_kw={"placeholder": "Enter email"})
    username = StringField("Username", validators=[InputRequired()], render_kw={"placeholder": "Enter username"})
    password = PasswordField("Password", validators=[InputRequired()], render_kw={"placeholder": "Enter password"})
    confirm = PasswordField("Confirm Password", validators=[InputRequired()], render_kw={"placeholder": "Confirm password"})
    submit = SubmitField("Register")

def editUser(user):
    class EditUser(FlaskForm):
        profile = StringField("Profile", validators=[InputRequired()], render_kw={"value" : user.ProfilePic})
        password = PasswordField("Password", validators=[Optional()], render_kw={"placeholder": "Enter password"})
        confirm = PasswordField("Confirm Password", validators=[Optional(), EqualTo(password)], render_kw={"placeholder": "Confirm password"})
        submit = SubmitField("Edit")

    return EditUser()

class Login(FlaskForm):
    username = StringField("Username", validators=[InputRequired()], render_kw={"placeholder": "Enter username"})
    password = PasswordField("Password", validators=[InputRequired()], render_kw={"placeholder": "Enter password"})
    submit = SubmitField("Login")

class CreateGroup(FlaskForm):
    name = StringField ("Name *", validators=[InputRequired(), Length(max=10, message="Max title length is 10")], render_kw={"placeholder": "Name of the group"} )
    pin = IntegerField("Pin (optional)", validators=[Optional()], render_kw={"placeholder": "Pin"})
    submit = SubmitField("Create")

class JoinGroup(FlaskForm):
    name = StringField ("Name *", validators=[InputRequired()], render_kw={"placeholder": "Name of the group"} )
    pin = IntegerField ("Pin *", validators=[InputRequired()], render_kw={"placeholder": "Pin"} )
    submit = SubmitField("Submit")

def editGroup(group):

    if group.Pin:
        class EditGroup(FlaskForm):
            name = StringField ("Name *", validators=[InputRequired()], render_kw={"value" : group.Name, "placeholder": "Name of the group"} ) 
            pin = IntegerField("Pin (optional)", validators=[Optional()], render_kw={"value" : group.Pin,"placeholder": "Pin (optional)"})
            submit = SubmitField("Submit")

        return EditGroup()
    else:
        class EditGroup(FlaskForm):
            name = StringField ("Name *", validators=[InputRequired()], render_kw={"value" : group.Name, "placeholder": "Name of the group"} ) 
            pin = IntegerField("Pin (optional)", validators=[Optional()], render_kw={"placeholder": "Pin (optional)"})
            submit = SubmitField("Submit")

        return EditGroup()

ALLOWED_FILE = {'PNG','JPG','png','jpg', 'JPEG', 'jpeg'}

class UploadImage(FlaskForm):
    image = FileField('Destination Image', validators=[FileRequired(), FileAllowed(ALLOWED_FILE)])
    submit = SubmitField("Upload")

class CreateComment(FlaskForm):
    comment = StringField ("Name *", validators=[InputRequired(), Length(max = 256)], render_kw={"placeholder": "Comment"} ) 
    submit = SubmitField("Post")

class DeleteEvent(FlaskForm):
    ID = IntegerField("ID", validators=[InputRequired()])
    submit = SubmitField("Delete")

class DeleteGroup(FlaskForm):
    ID = IntegerField("ID", validators=[InputRequired()])
    submit = SubmitField("Delete")


