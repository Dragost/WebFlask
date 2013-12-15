# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, flash, session, url_for, redirect
from forms import ContactForm, SigninForm, SignupForm, ProfileForm, AddcontactForm
from flask.ext.mail import Message, Mail
from models import Base, User, Contact
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps
from conf import *

# Configuración App
app = Flask(__name__)
app.config.from_object(__name__)

# Configuración Email
mail = Mail()
mail.init_app(app)

# Configuración SQL Alchemy
db = SQLAlchemy(app)
db.Model = Base

# Login decorator
def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if 'email' not in session:
      return redirect(url_for('signin', next=request.url))
    return f(*args, **kwargs)
  return decorated_function

# Rutas
@app.route('/', methods=['GET', 'POST'])
def signin():
  if 'email' in session:
    return redirect(url_for('contacts'))

  form = SigninForm()

  if request.method == 'POST':
    if form.validate(db) == False:
      return render_template('home.html', form=form)
    else:
      session['email'] = form.email.data
      return redirect(url_for('contacts'))

  elif request.method == 'GET':
    return render_template('home.html', form=form)

@app.route('/user/register', methods=['GET', 'POST'])
def signup():
  if 'email' in session:
    return redirect(url_for('contacts'))

  form = SignupForm(db=db)

  if request.method == 'POST':
    if form.validate(db) == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()

      session['email'] = newuser.email
      return redirect(url_for('contacts'))

  elif request.method == 'GET':
    return render_template('signup.html', form=form)

@app.route('/user/logout')
@login_required
def signout():
  session.pop('email', None)
  return redirect(url_for('signin'))

@app.route('/user/all')
def users():
  users = db.session.query(User).order_by(User.lastname.asc())
  return render_template('users.html', users=users)

@app.route('/user/delete')
@login_required
def removeacc():
  me = db.session.query(User).filter_by(email=session['email']).first()
  db.session.delete(me)
  db.session.commit()
  return signout()

@app.route('/user/profile', methods=['GET', 'POST'])
@login_required
def profile():
  form = ProfileForm()

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('profile.html', form=form)
    else:
      user = db.session.query(User).filter_by(email=session['email']).first()

      if form.firstname.data:
        user.firstname = form.firstname.data
      if form.lastname.data:
        user.lastname = form.lastname.data
      if form.password.data:
        user.set_password(form.password.data)

      db.session.commit()

      return redirect(url_for('contacts'))

  elif request.method == 'GET':
    return render_template('profile.html', form=form)

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()

  if request.method == 'POST':
    if form.validate() == False:
      flash('Todos los campos son obligatorios.')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.asunto.data, sender='tuemail@gmail.com', recipients=['destinatario'])

      msg.body = """
      De: %s <%s>
      %s
      """ % (form.nombre.data, form.email.data, form.mensaje.data)

      mail.send(msg)
      return render_template('contact.html', exito=True, nombre=form.nombre.data)
  elif request.method == 'GET':
    form = ContactForm()
    return render_template('contact.html', form=form)

@app.route('/contact/all')
@login_required
def contacts():
  contacts = db.session.query(Contact).order_by(Contact.lastname.asc())
  return render_template('contacts.html', contacts=contacts)

@app.route('/contact/add', methods=['GET', 'POST'])
@login_required
def addcontact():
  form = AddcontactForm()

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('addcontact.html', form=form)
    else:
      newcontact = Contact(form.firstname.data, form.lastname.data, form.email.data)
      db.session.add(newcontact)
      db.session.commit()

      return redirect(url_for('contacts'))

  elif request.method == 'GET':
    return render_template('addcontact.html', form=form)

# Manejo de errores
@app.errorhandler(404)
def notfound(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

# Lanzamos el servidor
if __name__ == '__main__':
    app.run(debug=True)