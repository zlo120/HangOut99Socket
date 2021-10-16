from enum import unique
from sqlalchemy.sql.schema import ForeignKey

from . import db

# Association tables
user_identifier = db.Table(
    'user_identifier',
    db.Column('hangoutgroup_id', db.Integer, db.ForeignKey('hangoutgroups.ID', ondelete='CASCADE') ),
    db.Column('user_id', db.Integer, db.ForeignKey('users.ID'))
)

interested_event = db.Table (
    'interested_events',
    db.Column('event_id', db.Integer, db.ForeignKey('events.ID', ondelete='CASCADE') ),
    db.Column('user_id', db.Integer, db.ForeignKey('users.ID'))
)

unavailable_event = db.Table(
    'unavailable_events',
    db.Column('event_id', db.Integer, db.ForeignKey('events.ID', ondelete='CASCADE') ),
    db.Column('user_id', db.Integer, db.ForeignKey('users.ID'))
)

class User(db.Model):
    __tablename__ = "users"
    ProfilePic = db.Column(db.String(256), nullable = False)
    ID = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement=True)
    Email = db.Column(db.String(256), nullable = False)
    Username = db.Column(db.String(256), unique = True, nullable = False)
    Password = db.Column(db.String(256), nullable = False)
    IsValidated = db.Column(db.Boolean, nullable = False)
	
    def __repr__(self):
        return f"{self.Username}"

    def get(self, id):
        return self.ID

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.ID

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

class HangOutGroup(db.Model):
    __tablename__ = "hangoutgroups"
    ID = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement=True)
    Creator_ID = db.Column(db.Integer, nullable = False)

    JoinLink = db.Column(db.String(256), nullable = False, unique = True)

    Pin = db.Column(db.Integer, nullable = True)

    Name = db.Column(db.String(256), nullable = False, unique = True)

    Users = db.relationship("User", secondary=user_identifier, backref="hangoutgroup")

    Events = db.relationship('Event', backref='hangoutgroup')
    
    def __repr__(self):
        return f"{self.Name}"

class Event(db.Model):
    __tablename__ = "events"
    ID = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement=True)
    Creator_ID = db.Column(db.Integer, nullable = False)
    Name = db.Column(db.String(256), nullable = False)
    Description = db.Column(db.String(256), nullable = False)
    DateTime = db.Column(db.DateTime, nullable = True)
    Location = db.Column(db.String(256), nullable = True)
    Link = db.Column(db.String(256), nullable = True)

    Users = db.relationship("User", secondary=interested_event, backref="event")    
    UnavailableUsers = db.relationship("User", secondary=unavailable_event, backref="unavailableEvent")    

    Comments = db.relationship("Comment", backref="Event")
    Photos = db.relationship("Photo", backref="Event")
    Hangout_ID = db.Column(db.String(256), db.ForeignKey('hangoutgroups.Name'))
    

    def __repr__(self):
        return f"{self.Name}"

class Photo(db.Model):
    __tablename__ = "photos"
    ID = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement=True)
    Creator_ID = db.Column(db.String(256), db.ForeignKey('users.Username'))
    Image = db.Column(db.String(400), nullable = False)

    Event_ID = db.Column(db.Integer, db.ForeignKey('events.ID'))

class Comment(db.Model):
    __tablename__ = "comments"
    ID = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement=True)
    Creator_ID = db.Column(db.String(256), db.ForeignKey('users.Username'))
    Content = db.Column(db.String(256), nullable = False)

    Event_ID = db.Column(db.Integer, db.ForeignKey('events.ID'))