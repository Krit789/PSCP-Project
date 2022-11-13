'''Flask Initialization'''
from flask import Flask
from flask_compress import Compress
from flask_sqlalchemy import SQLAlchemy
from os import path, getcwd
from flask_login import LoginManager

compress = Compress()
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    '''Create an instance of Flask app'''
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '4XSHacw5yf9YTy9oatd2TxH8'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .auth import auth
    
    app.register_blueprint(auth, url_prefix='/')
    compress.init_app(app)

    from .models import User, Note
    
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login_page'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print("Database Created!, this message will appear when database.db doesn't exist.")
    else:
        print('Database already exist! Skipping db creation...', getcwd())
