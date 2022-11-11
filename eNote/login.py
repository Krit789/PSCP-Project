from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound
from time import time as tme

login = Blueprint('login', __name__)

@login.route('/login', methods=['GET', 'POST'])
def login_page():
    rand_img = (int(str(tme()*1000)[-1])%4)+1
    try:
        if request.method == 'GET':
            return render_template('login.html', bg_img=rand_img)
        if request.method == 'POST':
            if len(request.form['user']) > 0 and len(request.form['passwd']) > 0:
                return render_template('login.html', bg_img=rand_img, data=True , var1=request.form['user'], var2=request.form['passwd'])
            return render_template('login.html', bg_img=rand_img, data=True , var1='N/A', var2='N/A')
    except TemplateNotFound:
        abort(404)