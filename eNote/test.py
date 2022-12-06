from os.path import abspath, dirname, join
DB_NAME = 'database.db'
print(join(abspath(dirname(__file__)), '..', str('instance/' + DB_NAME)))