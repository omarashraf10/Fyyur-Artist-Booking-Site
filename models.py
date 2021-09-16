import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy 
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
from datetime import datetime


app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Email1087@localhost:5432/example1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app,db)


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    #Genres
    genres = db.Column(db.ARRAY(db.String))
    #Website Link
    website = db.Column(db.String(120))
    #Looking for Talent 
    seeking_talent = db.Column(db.Boolean,default=False)
    #Seeking Description
    seeking_description = db.Column(db.String(500))

    Artists = db.relationship('Artist', secondary="shows",
    backref=db.backref('venues', lazy=True))


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    #Genres
    genres = db.Column(db.ARRAY(db.String))
    #Website Link
    website = db.Column(db.String(120))
    #Looking for Talent 
    seeking_venue = db.Column(db.Boolean, default=False)
    #Seeking Description
    seeking_description = db.Column(db.String(500))

    Venues = db.relationship('Venue', secondary="shows",
    backref=db.backref('artists', lazy=True))
class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer,primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)


def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime
