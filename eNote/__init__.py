from flask import Flask
from flask_compress import Compress

compress = Compress()



def create_app():
    app = Flask(__name__)
    compress.init_app(app)

    from .login import login

    app.register_blueprint(login, url_prefix='/')
    return app