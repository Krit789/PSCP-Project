'''Flask Initialization'''
from flask import Flask, render_template
from flask_compress import Compress
from flask_sqlalchemy import SQLAlchemy
from os.path import exists, abspath, dirname
from flask_login import LoginManager
import secrets

db = SQLAlchemy()
DB_NAME = "database.db"
UPLOAD_FOLDER = abspath(dirname(__file__)) + '/static/uploads'
# UPLOAD_FOLDER = '.\\uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def create_app():
    '''Create an instance of Flask app'''
    app = Flask(__name__)
    app.config['COMPRESS_MIMETYPES'] = ['text/html',
                                        'text/css',
                                        'text/xml',
                                        'application/json',
                                        'application/javascript',
                                        'image/svg+xml'
                                        ]
    app.config['COMPRESS_BR_LEVEL'] = 9
    app.config['SECRET_KEY'] = generate_secrets()
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    app.config['MAX_CONTENT_LENGTH'] = 8 * 1000 * 1000
    db.init_app(app)
    from .auth import auth
    from .pages import pages
    from .usr_profile import profile
    from .enote_core import core
    
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(pages, url_prefix='/')
    app.register_blueprint(profile, url_prefix='/')
    app.register_blueprint(core, url_prefix='/')
    from .models import User
    
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login_page'
    login_manager.init_app(app)
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("error404.html", error_code=404, custom_bg='background: linear-gradient(0deg, rgba(255,0,0,0.2) 35%, rgba(121,16,9,0.5) 80%, rgba(152,20,0,0.8) 100%);', error_desc='This page does not exist'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("error404.html", error_code=403, custom_bg='background: linear-gradient(0deg, rgba(255,0,0,0.2) 35%,, rgba(121,16,9,0.5) 80%, rgba(152,20,0,0.8) 100%);', error_desc='You don\'t have permission to access this page'), 403

    @login_manager.user_loader
    def load_user(session_token):
        return User.query.filter_by(session_token=session_token).first()
    compress = Compress()
    compress.init_app(app)
    return app

def generate_secrets() -> str:
    '''Generate a cryptographically secure secrets in instance folder'''
    if not exists('instance/secrets'):
        print("Secrets not generated yet. Generating secrets...")
        with open('instance/secrets', 'w') as f:
            conf_secret = secrets.token_hex() 
            f.write(conf_secret)
    else:
        print("Secrets already generated")
        with open('instance/secrets', 'r') as f:
            conf_secret = f.read()
    return conf_secret

def create_database(app):
    if not exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Database Created!")
    else:
        print('Database already exist!')