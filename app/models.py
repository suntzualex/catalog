from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
from flask_login import UserMixin

Base = declarative_base()

class Category(Base):
    __tablename__='Category'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(2048), nullable=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Category> %d>' % self.id

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class Item(Base):
    __tablename__='Item'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(2048), nullable=False)
    category = Column(Integer, ForeignKey('Category.id'))
    creator =  Column(Integer, ForeignKey('User.social_id'))
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, title, description, category, creator):
        self.title = title
        self.description = description
        self.category = category
        self.creator = creator

    def __repr__(self):
        return '<Item> %d>' % self.id

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'creator': self.creator,
            'creation_date': self.creation_date
        }


class User(UserMixin, Base):
    __tablename__='User'
    id = Column(Integer, primary_key=True)
    social_id = Column(Integer, nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)

    def __init__(self, social_id, name, email):
        self.name = name
        self.social_id = social_id
        self.email = email

    def __repr__(self):
        return '<User %d,social_id %d, name %s, email %s'\
                %(self.id, self.social_id, self.name, self.email)
