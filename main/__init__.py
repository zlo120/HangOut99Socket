from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import json
import os 

app = None
db = SQLAlchemy()
bcrypt = None
login_manager = LoginManager()

def initialize_db():
    global app
    global db
    global bcrypt
    global login_manager

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db = SQLAlchemy(app)

    return app, db

def create_app():
    global app
    global db
    global bcrypt
    global login_manager

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'AIzaSyDdkNpKFJt2n8M0gzbWp4q2LbJr1f73rso'
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_DATABASE_URI']  = 'sqlite:///site.db'

    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)
    bcrypt = Bcrypt(app)
    login_manager.init_app(app)

    from . import user, event, routes, hangout, error_handlers

    app.register_blueprint(user.userbp)
    app.register_blueprint(event.eventbp)
    app.register_blueprint(routes.mainbp)
    app.register_blueprint(hangout.hangoutbp)

    app.register_error_handler(404, error_handlers.page_not_found)
    app.register_error_handler(401, error_handlers.not_authenticated)
    
    @app.route('/favicon.ico')
    def favicon():  
        return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

    return app