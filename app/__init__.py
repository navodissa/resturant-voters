from flask import Flask
#from app import routes
#from config import basedir
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Message, Mail
import os


app = Flask(__name__)
app.secret_key = 'development key'
app.config.from_object('config')
db = SQLAlchemy(app)
mail = Mail(app)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'noreplyresturantvoters@gmail.com'
app.config["MAIL_PASSWORD"] = 'aqdesw@123'



#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://your-username:your-password@localhost/development'
from app import routes,models
