from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_bcrypt import Bcrypt  


app = Flask(__name__)
app.secret_key = "guitar"
bcrypt = Bcrypt(app)