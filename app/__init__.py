from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
#Flask admin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
#flask basic auth
from flask_basicauth import BasicAuth
from flask import Response


#mail = Mail()

db = SQLAlchemy()
admin = Admin(name='prelaunchr', template_mode='bootstrap3')
basic_auth = BasicAuth()

# extend admin views to support flask-BasicAuth
from werkzeug.exceptions import HTTPException

class AuthException(HTTPException):
    def __init__(self, message):
        super(AuthException, self).__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))

class ModelView(ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    # flask admin
    from models import User, Referrer, IPAddress
    admin.init_app(app)
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Referrer, db.session))
    admin.add_view(ModelView(IPAddress, db.session))
    # basic auth
    basic_auth.init_app(app)
    # proxy fix
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)

    from .main import main as main_blueprint
    #
    app.register_blueprint(main_blueprint)


    return app
