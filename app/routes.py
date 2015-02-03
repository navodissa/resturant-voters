#!flask/bin/python3
from app import app
from flask import render_template, request, flash, session, url_for, redirect
from app.forms import ContactForm, SignupForm, SigninForm, ResturantForm, OrderForm, AdminForm
import string, datetime
from app.models import db, User, sel_resturant, Resturant, Menu, Orders, SelectResturant, TempOrders, Tempsel_resturant
from flask.ext.mail import Message, Mail
from sqlalchemy.exc import IntegrityError

mail = Mail(app)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'noreplyresturantvoters@gmail.com'
app.config["MAIL_PASSWORD"] = 'aqdesw@123'

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()

  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender='contact@example.com', recipients=['your_email@example.com'])
      msg.body = """
      From: %s <%s>
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)

      return render_template('contact.html', success=True)

  elif request.method == 'GET':
    return render_template('contact.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()

  if 'email' in session:
    return redirect(url_for('profile'))

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()

      session['email'] = newuser.email
      return redirect(url_for('profile'))

  elif request.method == 'GET':
    return render_template('signup.html', form=form)


@app.route('/profile', methods=['GET','POST'])
def profile():
  if 'email' not in session:
    return redirect(url_for('signin'))

  user = User.query.filter_by(email = session['email']).all()
  for u in user:
      name = u.firstname

  form = ResturantForm()
  output = "Please vote for your resturant"
  if request.method == 'POST':
    try:
        a = User.query.filter_by(email = session['email']).all()
        for u in a:
            name = u.firstname
        resturant = form.resturant.data
        now = datetime.datetime.now()
#        selectedres = sel_resturant(name, session['email'], resturant, now)
        temp_selectedres = Tempsel_resturant(name, session['email'], resturant)
#        db.session.add(selectedres)
        db.session.add(temp_selectedres)
        db.session.commit()
        return redirect(url_for('order'))
    except IntegrityError:
        error = 'You have already voted.'
        return render_template('profile.html', form=form, name=name, error=error)
    except AttributeError:
        error = 'You have not voted yet to delete any.'
        return render_template('profile.html', form=form, name=name, error=error)
  else:
    if user is None:
      return redirect(url_for('signin'))
    else:
      return render_template('profile.html', form=form, name=name, output=output)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()

  if 'email' in session:
    return redirect(url_for('profile'))

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['email'] = form.email.data
      return redirect(url_for('profile'))

  elif request.method == 'GET':
    return render_template('signin.html', form=form)


@app.route('/signout')
def signout():

  if 'email' not in session:
    return redirect(url_for('signin'))

  session.pop('email', None)
  return redirect(url_for('home'))


@app.route('/order', methods=['GET','POST'])
def order():
    if request.method == 'GET':
        try:
            a = User.query.filter_by(email = session['email']).all()
            for u in a:
                name = u.firstname
            b = Tempsel_resturant.query.filter_by(email = session['email']).all()
            for u in b:
                res = u.resturant
            resturant = res
            email = session['email']
            count_mc = Tempsel_resturant.query.filter_by(resturant='McDonald').count()
            count_dine = Tempsel_resturant.query.filter_by(resturant='Dinemore').count()
            count_pizza = Tempsel_resturant.query.filter_by(resturant='Pizza Hut').count()
            count_great = Tempsel_resturant.query.filter_by(resturant='Great Wall').count()
            count_steam = Tempsel_resturant.query.filter_by(resturant='Steam Boat').count()
            count_dragon = Tempsel_resturant.query.filter_by(resturant='Chinese Dragon').count()

            count = {'mc' : count_mc,
                    'dine' : count_dine,
                    'pizza' : count_pizza,
                    'great' : count_great,
                    'steam' : count_steam,
                    'dragon' : count_dragon
                    }

            data = {'name' : name,
                    'email' : email,
                    'resturant' : resturant
                    }
    #            return redirect(url_for('done.html'))
            return render_template('done.html', data=data, count=count)
        except KeyError:
            return redirect('/signin')


@app.route('/delete', methods=['GET','POST'])
def user():
    try:
        a = User.query.filter_by(email = session['email']).all()
        for u in a:
            name = u.firstname
        try:
            if request.method == 'GET':
                delname = Tempsel_resturant.query.filter_by(name=name).first()
                delres = delname.resturant
                deletename = "Active"
                return render_template("delete_order.html",delname=delres, deletename=deletename)
        except AttributeError:
            return redirect('/signin')
        if request.method == 'POST':
            Tempsel_resturant.query.filter_by(name=name).delete()
            sel_resturant.query.filter_by(name=name).delete()
            db.session.commit()
            deletename = "Deleted"
            return render_template("delete_order.html",deletename=deletename)
    except KeyError:
        return redirect('/signin')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = AdminForm(request.form)
    if request.method == 'GET':
        count_mc = Tempsel_resturant.query.filter_by(resturant='McDonald').count()
        count_dine = Tempsel_resturant.query.filter_by(resturant='Dinemore').count()
        count_pizza = Tempsel_resturant.query.filter_by(resturant='Pizza Hut').count()
        count_great = Tempsel_resturant.query.filter_by(resturant='Great Wall').count()
        count_steam = Tempsel_resturant.query.filter_by(resturant='Steam Boat').count()
        count_dragon = Tempsel_resturant.query.filter_by(resturant='Chinese Dragon').count()

        count = {'mc' : count_mc,
                'dine' : count_dine,
                'pizza' : count_pizza,
                'great' : count_great,
                'steam' : count_steam,
                'dragon' : count_dragon
                }
        return render_template("admin.html", form=form, count=count)
    else:
        SelectResturant.query.delete()
        db.session.commit()
        admin_res = str(form.selectedRes.data)
        newuser = SelectResturant(admin_res.replace("'",""))
        db.session.add(newuser)
        db.session.commit()
        abc = admin_res.replace("'","")
        count_mc = Tempsel_resturant.query.filter_by(resturant='McDonald').count()
        count_dine = Tempsel_resturant.query.filter_by(resturant='Dinemore').count()
        count_pizza = Tempsel_resturant.query.filter_by(resturant='Pizza Hut').count()
        count_great = Tempsel_resturant.query.filter_by(resturant='Great Wall').count()
        count_steam = Tempsel_resturant.query.filter_by(resturant='Steam Boat').count()
        count_dragon = Tempsel_resturant.query.filter_by(resturant='Chinese Dragon').count()

        count = {'mc' : count_mc,
                'dine' : count_dine,
                'pizza' : count_pizza,
                'great' : count_great,
                'steam' : count_steam,
                'dragon' : count_dragon
                }
        if abc != 'None':
            a = User.query.filter_by(email = session['email']).all()
            for u in a:
                name = u.firstname
            user_mails = Tempsel_resturant.query.all()
            cou = Tempsel_resturant.query.count()
            if form.user_email.data == "":
                return render_template("admin.html", form=form, count=count, abc = user_mails)
            else:
                mills = [form.user_email.data]
    #            mills = str(user_mails)
    #            mills = mills.replace("[","")
    #            mills = mills.replace("]","")
        #            return render_template("admin.html", form=form, count=count, abc = mills)
                send_email("[Resturant Voters] %s is chosen" % abc,
                            'navomails@gmail.com',
                            mills,
                            render_template("mail_body_all.txt", rest=abc, count=count, name=name))
        return render_template("admin.html", form=form, count=count, abc = abc)


def send_email(subject, sender, recipients, text_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    mail.send(msg)


@app.route('/resturant', methods=['GET','POST'])
def resturant():
#    res = Resturant.query.all()
#    menu = Menu.query.filter_by(resturant='Pizza Hut').all()
#    if request.method =='GET':
#        return render_template("make_order.html", res=res, me=menu)

    form = OrderForm()
    if request.method == 'POST':
        try:
            a = User.query.filter_by(email = session['email']).all()
            for u in a:
              name = u.firstname
            b = SelectResturant.query.all()
            b = str(b)
            b = b.replace("[","")
            b = b.replace("]","")
            b = b.replace("'","")
            menu = str(form.sel_menu.data)
            menu_r = menu.replace("'","")
            if menu_r !='None':
                TempOrders.query.filter_by(email = session['email']).delete()
                db.session.commit()
                send_email("[ukst foods] %s is your choice" % menu_r,
                         'navomails@gmail.com',
                         [session['email']],
                         render_template("mail_body.txt",
                                         name=name, menu=menu_r, b=b))
                now = datetime.datetime.now()
                TempOrders.query.filter_by(email=session['email']).delete()
                db.session.commit()
                newuser = Orders(name, session['email'],b , menu_r, now)
                temporder = TempOrders(name, session['email'], b, menu_r)
                db.session.add(newuser)
                db.session.add(temporder)
                db.session.commit()
                return redirect('/')
            return redirect('/resturant')
        except KeyError:
            return redirect('/signin')
    else:
      b = SelectResturant.query.all()
      b = str(b)
      b = b.replace("[","")
      b = b.replace("]","")
      b = b.replace("'","")
      if b=="None":
          error = "Please vote for the resturant first."
          error2 = "Once everyone is done voting, menu selection will be activated."
          return render_template("make_order.html", form=form, b=b, error=error, error2=error2)
      return render_template("make_order.html", form=form, b=b)


@app.route('/delete_all', methods=['GET','POST'])
def delete_all():
    if request.method == 'POST':
        TempOrders.query.delete()
        Tempsel_resturant.query.delete()
        db.session.commit()
        return redirect('/')
    else:
        return render_template("delete_all.html")


@app.route('/view_all', methods=['GET','POST'])
def view_all():
    if request.method == 'POST':
        all_menu = TempOrders.query.filter(TempOrders.email.endswith('.com')).order_by(TempOrders.food).all()
        return render_template("view_all.html", uname=all_menu)
    else:
        all_menu = TempOrders.query.filter(TempOrders.email.endswith('.com')).order_by(TempOrders.food).all()
        return render_template("view_all.html", uname=all_menu)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
