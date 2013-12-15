# -*- coding: utf-8 -*-

# Clave para formularios
SECRET_KEY = ""

# Email
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = '' # Correo
MAIL_PASSWORD = '' # Contraseña

# Conexión a la bbdd
SQLALCHEMY_DATABASE_URI = 'mysql://Usuario:Contraseña@localhost/webflask' # Usuario:Contraseña

# Recaptcha
RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = '6LeJmeoSAAAAAGAv9mSzRk-mKEE3I8i1LoqjClcA'
RECAPTCHA_PRIVATE_KEY = '6LeJmeoSAAAAAG38d7TBJqN5TPumnh80pVYwORL3'
RECAPTCHA_OPTIONS = {'theme': 'white'}