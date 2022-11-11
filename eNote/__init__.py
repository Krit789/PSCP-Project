from flask import Flask
from flask_compress import Compress

compress = Compress()

def create_app():
    app = Flask(__name__)
    
    from .auth import auth

    app.register_blueprint(auth, url_prefix='/')
    compress.init_app(app)
    return app