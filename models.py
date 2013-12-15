# -*- coding: utf-8 -*-

from werkzeug import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column
from sqlalchemy import DateTime, Integer, String, Text

Base = declarative_base()

class User(Base):
  __tablename__ = 'users'
  uid = Column(Integer, primary_key=True)
  firstname = Column(String(100))
  lastname = Column(String(100))
  email = Column(String(120), unique=True)
  pwdhash = Column(String(100))

  def __init__(self, firstname, lastname, email, password):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password)

  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)

class Contact(Base):
  __tablename__ = 'contacts'
  cid = Column(Integer, primary_key=True)
  firstname = Column(String(100))
  lastname = Column(String(100))
  email = Column(String(120))

  def __init__(self, firstname, lastname, email):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()