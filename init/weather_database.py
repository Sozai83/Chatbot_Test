from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import pandas as pd
import numpy as np
from datetime import datetime
from __main__ import db, app


class WeatherDB(db.Model):
    __tablename__ = 'weather'
    weather_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.Text)
    created_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    cur_temp = db.Column(db.Float, nullable=True)
    min_temp = db.Column(db.Float, nullable=False)
    max_temp = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    icon = db.Column(db.Text, nullable=False)
    pop = db.Column(db.Text, nullable=True)



class LocationDB(db.Model):
    __tablename__ = 'location'
    location = db.Column(db.Text, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    country = db.Column(db.Text)

def create_db():
    with app.app_context():
        db.create_all()

def add_weather(location, date, desc, min_temp, max_temp, humidity, icon, cur_temp=None, pop=None):
    
    temp_weather = WeatherDB(
        location = location,
        date = date,
        desc = desc,
        cur_temp = cur_temp,
        min_temp = min_temp,
        max_temp = max_temp,
        humidity = humidity,
        icon = icon,
        pop = pop
    )

    db.session.add(temp_weather)
    db.session.commit()



def add_location(location, latitude, longitude, country='UK'):

    temp_location = LocationDB(
        location = location,
        latitude = latitude,
        longitude = longitude,
        country = country
    )

    db.session.add(temp_location)
    db.session.commit()
