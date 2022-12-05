'''For use in production. Powered by FastWSGI'''
from eNote import create_app
import fastwsgi

app = create_app()

if __name__ == '__main__':
    fastwsgi.run(wsgi_app=app, host='0.0.0.0', port=5000)
