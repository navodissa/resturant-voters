from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, RadioField, SubmitField, validators, ValidationError, PasswordField, SelectField, StringField
from app.models import db, User, sel_resturant, Resturant, Menu, SelectResturant
from wtforms.ext.sqlalchemy.fields import QuerySelectField
#from routes import admin_res
import string,re

class ContactForm(Form):
  name = TextField("Name",  [validators.Required("Please enter your name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  subject = TextField("Subject",  [validators.Required("Please enter a subject.")])
  message = TextAreaField("Message",  [validators.Required("Please enter a message.")])
  submit = SubmitField("Send")

class SignupForm(Form):
  firstname = TextField("First name",  [validators.Required("Please enter your first name.")])
  lastname = TextField("Last name",  [validators.Required("Please enter your last name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Create account")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    e_mail = self.email.data.lower()
    if not Form.validate(self):
      return False

    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("That email is already taken")
      return False
    elif not re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@gmail.com",e_mail):
      self.email.errors.append("Please enter a valid Virtusa mail address")
      return False
    else:
      return True

class SigninForm(Form):
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Sign In")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False

    user = User.query.filter_by(email = self.email.data).first()
    if user and user.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False

class ResturantForm(Form):
    resturant = RadioField('Resturant', choices=[('Pizza Hut','Pizza Hut'),
                                                 ('Chinese Dragon','Chinese Dragon'),
                                                 ('McDonald','McDonald'),
                                                 ('Dinemore','Dinemore'),
                                                 ('Great Wall','Great Wall'),
                                                 ('Steam Boat','Steam Boat')])
    submit = SubmitField("Confirm")

def possible_res():
    return Resturant.query

def possible_menu():
    abc = SelectResturant.query.first()
    return Menu.query.filter_by(resturant=abc.resturant)

def selected_res():
    return SelectResturant.query

class OrderForm(Form):

#    sel_res = QuerySelectField(query_factory=selected_res,
#                               get_label="resturant")

    sel_menu = QuerySelectField(query_factory=possible_menu,
                                get_label="food")

    submit = SubmitField("Confirm")

    def __init__(self, *args, **kwargs):
      Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
          return False


#    sel_res = SelectField('Selected Resturant', choices = [(1, "Pizza Hut"),(2,"KFC"),(3,"McDonald")])

class AdminForm(Form):
    selectedRes = QuerySelectField(query_factory=possible_res,
                                   get_label="name",
                                   allow_blank=True)
    user_email = TextField("Email")
    submit = SubmitField("Confirm")

    def __init__(self, *args, **kwargs):
      Form.__init__(self, *args, **kwargs)
