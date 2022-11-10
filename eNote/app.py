from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        return render_template('login.html',data=True , var1=request.form['user'], var2=request.form['passwd'])




if __name__ == '__main__':
    app.run(debug=True)