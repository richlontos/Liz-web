from flask_app import app, render_template, request, redirect, session, bcrypt, flash
from flask import abort, make_response, url_for
from flask_app.models.user import User
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from flask_dance.contrib.github import make_github_blueprint, github 
import os
import pathlib
import requests
from random import random


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "670699670743-5kagjkr891ilkbba090njvgtu3r08cl1.apps.googleusercontent.com"
client_secret_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")


flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secret_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)





app.config["SECRET_KEY"]="SECRET KEY  "

github_blueprint = make_github_blueprint(client_id='c6a874a2a6dadcf0f6d5',
                                         client_secret='0c525fa5cea8a81ea1bf6b178585b9537e8ddb21')

app.register_blueprint(github_blueprint, url_prefix='/github/login')





def login_is_required(function):

        def wrapper(*args, **kwargs):
            if "google_id" not in session:
                return abort(401)  # Authorization required
            else:
                return function()

        return wrapper


# TODO ROOT ROUTE
@app.route('/')
def index():
    return render_template('index.html')



# TODO REGISTER
@app.route('/register/user', methods = ['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')

    hashed_pw = bcrypt.generate_password_hash(request.form['password'])

    user_data = {
        'first_name': request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password': hashed_pw
    }

    user_id = User.save(user_data)
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']

    return redirect('/programs')


# TODO LOGIN
@app.route('/login', methods = ['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("invalid credentials")
        return redirect('/login/page')
    password_valid = bcrypt.check_password_hash(user.password, request.form['password'])

    if not password_valid:
        flash("invalid credentials")
        return redirect('/login/page')
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name


    return redirect('/')



@app.route('/register/page')
def register_page():
    return render_template('register.html')


@app.route('/login/page')
def login_page():
    return render_template('log_in.html')


@app.route('/google/login')
def google_login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/")

# @app.route('/protected/area')
# @login_is_required
# def protected_area():
#     return 'Protected'

# @app.route('/test')
# def test():
#     return "Hello world <a href='/google/login'><button>Login</button></a>"



@app.route('/github/login')
def github_login():

    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
        account_info = github.get('/')
        if account_info.ok:
            account_info_json = account_info.json()
            return '<h1>Your Github name is {}'.format(account_info_json['login'])

    return '<h1>Request failed!</h1>'

 



