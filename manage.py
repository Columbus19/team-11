from flask import (
    Flask, render_template,
    redirect, request,
    flash, session,
    jsonify
)

from utils.forms import (
    LoginForm, SignUpForm,
    ChangeEmailForm, ChangePasswordForm
)

from flask_restful import Resource, Api, reqparse
from utils.decorators import login_required
from flask_pagedown import PageDown
from flask import Markup
import utils.functions as functions
from werkzeug.utils import secure_filename

import datetime
import markdown
import random
# import pdftables_api
import pandas as pd
import os

app = Flask(__name__)
api = Api(app)
pagedown = PageDown(app)
parser = reqparse.RequestParser()
app.secret_key = str(random.randint(1, 20))
app.config['MAX_CONTENT_LENGTH'] = 55 * 1024 * 1024
UPLOAD_FOLDER = '.'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(os.path.join(app.instance_path), exist_ok=True)


@app.route('/')
@app.route('/homepage')
def home_page():
    '''
        App for hompage
    '''
    session['user_count'] = functions.get_user_count()
    try:
        if session['username']:
            return render_template('homepage.html', username=session['username'])
        return render_template('homepage.html')
    except (KeyError, ValueError):
        return render_template('homepage.html')


@app.route('/login/', methods=('GET', 'POST'))
def login():
    '''
        App for creating Login page
    '''
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = functions.generate_password_hash(request.form['password'])
        user_id = functions.check_user_exists(username, password)
        if user_id:
            session['username'] = username
            session['id'] = user_id
            functions.store_last_login(session['id'])
            return redirect('/')
        else:
            flash('Username/Password Incorrect!')
    return render_template('login.html', form=form)


@app.route('/signup/', methods=('GET', 'POST'))
def signup():
    '''
        App for registering new user
    '''
    form = SignUpForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = functions.generate_password_hash(request.form['password'])
        email = request.form['email']
        check = functions.check_username(username)
        if check:
            flash('Username already taken!')
        else:
            functions.signup_user(username, password, email)
            session['username'] = username
            user_id = functions.check_user_exists(username, password)
            session['id'] = user_id
            return redirect('/login')
    return render_template('signup.html', form=form)


@app.route("/logout/")
def logout():
    '''
        App for logging out user
    '''
    session['username'] = None
    session['id'] = None
    return login()


@app.route("/profile/settings/change_email/", methods=['GET', 'POST'])
@login_required
def change_email():
    '''
        App for changing the email of a user
    '''
    form = ChangeEmailForm()
    if form.validate_on_submit():
        email = request.form['email']
        functions.edit_email(email, session['id'])
        return redirect('/profile/settings/')
    return render_template('change_email.html', form=form, username=session['username'])


@app.route("/profile/settings/change_password/", methods=['GET', 'POST'])
@login_required
def change_password():
    '''
        App for changing the password of a user
    '''
    form = ChangePasswordForm()
    if form.validate_on_submit():
        password = request.form['password']
        functions.edit_password(password, session['id'])
        return redirect('/profile/settings/')
    return render_template('change_password.html', form=form, username=session['username'])


@app.route('/uploader', methods = ['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        # c = pdftables_api.Client('5niw5iiwxvgk')
        filepath = os.path.join(app.instance_path, secure_filename(file.filename))
        # saves file to be opened by pdftohtml converter
        file.save(filepath)
        # converts pdf to html
        temp = c.html(filepath)
        # converts html to pandas dataframe
        df = pd.read_html(temp)
        # data preproccessing
        df = pd.concat(df)
        df.columns = ['date', 'description', 'location', 'temp', 'amount', 'balance']
        df = df.dropna(subset=['date'])
        df = df[df['date'].map(len) < 6]
        df.location.fillna(df.description, inplace=True)
        del df['description']
        del df['temp']
        df.set_index('date', inplace=True)
        df.reset_index(inplace=True)
        user_id = session['id']
        df['parent_id'] = user_id
        # deletes saved pdf file
        os.remove(filepath)

        print(df)
        conn = functions.get_database_connection()
        df.to_sql(name='debt', con=conn, index=False, if_exists='append')


        return render_template('bank_data.html')


@app.route('/bank_data/', methods = ['GET', 'POST'])
@login_required
def bank_data():
    return render_template('bank_data.html')


if __name__ == '__main__':
    app.run()
