from flask import Flask, request, render_template
from time import time as tme
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World'

@app.route('/login', methods=['GET', 'POST'])
def login():
    rand_img = (int(str(tme()*1000)[-1])%4)+1
    if request.method == 'GET':
        return render_template('login.html', bg_img=rand_img)
    if request.method == 'POST':
        return render_template('login.html', bg_img=rand_img, data=True , var1=request.form['user'], var2=request.form['passwd'])




if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
