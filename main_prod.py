'''For use in production. Powered by waitress'''
from eNote import create_app
from waitress import serve

app = create_app()

if __name__ == '__main__':
    serve(app=app, host='0.0.0.0', port=5000)
