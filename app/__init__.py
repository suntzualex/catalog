from flask import Flask
from flask import render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import authentication
from models import Base

app = Flask(__name__)
app.config['SECRET_KEY'] = "super_secret_key"
app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': '326861684438397',
        'secret': '086e6980ab1a1705d46a3b8eccedd767'
    },
    'twitter': {
        'id': 'RSY25MYFWqQlbomtNmxxy71a9',
        'secret': '1bhcL4TzsTPOOugaR411EU7frE2SGrzep5WyTfoWXHdyYLrGi3'
    },
    'google':{
        'id': '78419860005-fjssrgcr626qpmk4feic9snbss1og6np.apps.googleusercontent.com',
        'secret': 'vXmoJiVcB3mJ7mrMCH23leT-'
    }
}

# connect to database and create database session
engine = create_engine('postgresql://catalog:pass@localhost/catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db=DBSession()

import models
import database
from database import init_database
from main import views
from main import database_operations
