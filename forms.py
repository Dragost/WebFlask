# -*- coding: utf-8 -*-

from flask_wtf import Form, RecaptchaField
from wtforms import TextField, TextAreaField, SubmitField, PasswordField, validators
from models import User

class ContactForm(Form):
  nombre = TextField("Nombre", [validators.Required("Introduzca el Nombre")])
  email = TextField("Email",  [validators.Required("Introduzca el email"), validators.Email("Introduzca email correctamente")])
  asunto = TextField("Asunto", [validators.Required("Introduzca asunto")])
  mensaje = TextAreaField("Mensaje", [validators.Required("introduzca mensaje")])
  enviar = SubmitField("Enviar")

class SigninForm(Form):
  email = TextField("Email",  [validators.Required("Introduce tu email."), validators.Email("Introduce tu email.")])
  password = PasswordField(u"Contraseña", [validators.Required(u"Introduce una contraseña.")])
  submit = SubmitField("Entrar")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self, db):
    if not Form.validate(self):
      return False

    user = db.session.query(User).filter_by(email = self.email.data.lower()).first()
    if user and user.check_password(self.password.data):
      return True
    elif not user:
      self.email.errors.append("Ese usuario no existe")
      return False
    else:
      self.email.errors.append(u"Email y/o contraseña incorrectos")
      return False

class SignupForm(Form):
  firstname = TextField("Nombre",  [validators.Required("Introduce tu nombre.")])
  lastname = TextField("Apellido",  [validators.Required("Introduce tu apellido.")])
  email = TextField("Email",  [validators.Required("Introduce tu email."), validators.Email("Please enter your email address.")])
  password = PasswordField(u"Contraseña", [validators.Required(u"Introduce una contraseña.")])
  recaptcha = RecaptchaField()
  submit = SubmitField("Registrarse")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self, db):
    if not Form.validate(self):
      return False

    user = db.session.query(User).filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("Ese email ya esta en uso.")
      return False
    else:
      return True

class ProfileForm(Form):
  firstname = TextField("Nombre",  [validators.Required("Introduce el nombre.")])
  lastname = TextField("Apellido",  [validators.Required("Introduce el apellido.")])
  password = PasswordField(u"Contraseña", [validators.Required(u"Introduce una contraseña.")])
  submit = SubmitField("Guardar")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False
    else:
      return True

class AddcontactForm(Form):
  firstname = TextField("Nombre",  [validators.Required("Introduce el nombre.")])
  lastname = TextField("Apellido",  [validators.Required("Introduce el apellido.")])
  email = TextField("Email",  [validators.Required("Introduce el email."), validators.Email("Please enter your email address.")])
  submit = SubmitField("Guardar")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False
    else:
      return True