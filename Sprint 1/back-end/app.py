from flask import Flask, render_template, request, redirect,url_for, flash



app = Flask(__name__)


@app.route('/')
def index():
    render_template('main.html')

@app.route('/provider', methods=['GET', 'POST'])
def provider():


    return render_template('provider.html')


@app.route('/new-user', methods=['GET', 'POST'])
def new_user():


    return render_template('new-user.html')


@app.route('/login', methods=['GET', 'POST'])
def login():


    return render_template('login.html')



if __name__ == '__main__':
    app.run(debug=True)