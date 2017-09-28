from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, asc, desc
import sys
from flask import jsonify
from app.models import Base, Category, Item, User
from app import app
from app import db as session

class DatabaseOperations:

    """
       Functions related to the User Table.
    """
    def addUser(self, social_id, name, email):
        # check if user exists with the same name.
        newUser = User(social_id=social_id, name=name, email=email)
        session.add(newUser)
        session.commit()
        if newUser:
            return newUser
        return None

    def getUserBySocialId(self, social_id):

        return session.query(User).filter_by(social_id=social_id).first()

    def getUserById(self, id):

        return session.query(User).filter_by(id=id).first()

    def getUserName(self, id):

        user = session.query(User).filter_by(id=id).first()
        if user:
            return user.name
        else:
            return ""

    def getItemsOfUser(self, id):

        user = self.getUserById(id=id)
        user_items = []
        if user:
            for item in self.getAllItems():
                if self.isCreator(item.id, user):
                    user_items.append(item)
        return user_items

    def getNumberOfItemsPerCategory(self, category_id):
        return session.query(Item).filter_by(category=category_id).count()


    def getNumberOfItemsOfUser(self, user):
        if not user:
            return False
        item_list = self.getItemsOfUser()
        return len(item_list)

    def getUserIdByMail(self, email):

        user = session.query(User).filter_by(email=email).first()
        if user:
            return user.id
        else:
            return None
    """
       Category related functions
    """
    def getCategories(self):
        return session.query(Category).all()

    def getCategoryById(self, id):
        return session.query(Category).filter_by(id=id).first()

    def getCategoryDescription(self, id):
        category = session.query(Category).filter_by(id=id).first()
        if category:
            if category.description:
                return category.description
            else:
               return "There is no description for this category."
        return "This category does not exist."

    def getNumberOfCategories(self):
        return session.query(Category).all().count()

    def getNumberOfCategoriesOfUser(self, user):
        category_list = []
        if not user:
            return False

        for item in self.getNumberOfItemsOfUser(user):
            category = item.category
            if category not in category_list:
                return ""
            else:
                category_list.append(category)
            return len(category_list)

    def getExistingCategories(self):
        categories = self.getCategories()
        categoryList = []
        for category in categories:
            categoryList.append(category.id)
        return categoryList

    """
       Item related Functions
    """

    def getItemById(self, id):
        return session.query(Item).filter_by(id=id).first()

    def getCategoryForItem(self, item):
        id = item.category
        category = session.query(Category).filter_by(id=id).first()
        if category:
            name = category.name
        else:
            name = ''
        return name

    def getItemCreator(self, id):
        item = session.query(Item).filter_by(id=id).first()
        if item:
            return item.creator
        else:
            return None

    def getCategoryTitles(self, category):
        titles = []
        for item in self.getItemsForCategory(category):
            titles.append(item.title)
        return titles

    def getItemsForCategory(self, category):
        return session.query(Item).filter_by(category=category).all()

    def getLatestItems(self, number):
        return session.query(Item).order_by\
                            (desc(Item.creation_date)).limit(number)

    def getAllItems(self):
        return session.query(Item).all()

    """
       Check if item exists in all Categories.
       This must be changed if there is a possibility of having
       the same item for different categories.
    """
    def existingItem(self, item):
        # actually we should check for an item being a real
        # item having all the properties of item.
        if item is None:
            return False
        # the item is the same if title and description are the same
        for existing_item in session.query(Item).all():
            if (item.title == existing_item.title) and\
               (item.description == existing_item.description):
                return True
        return False

    def addItem(self, item):
        # check if incoming item is not None
        if item is None:
            return False
        # check if item already exists
        if self.existingItem(item):
            return False
        if item.title == '':
            return False
        if item.description == '':
            return False
        # After all these checks have passed create the item.
        session.add(item)
        session.commit()
        return True


    def isCreator(self, id, user):

        item = self.getItemById(id)
        if not item:
            return False
        # if the user is not the creator or the item is None return False
        if user.social_id != item.creator:
            return False
        return True


    def deleteItem(self, id, user):
        # only creator of the item can delete items
        if not(self.isCreator(id, user)):
            return False
        item = session.query(Item).filter_by(id=id).first()
        session.delete(item)
        session.commit()
        return True

    def updateItem(self, old_item_id, updated_item, user):

        if not(self.isCreator(old_item_id, user)):
            return False
        old_item = session.query(Item).filter_by(id=old_item_id).first()
        if not old_item:
            return False
        # delete old item
        self.deleteItem(old_item_id, user)
        # add updated item
        session.add(updated_item)
        session.commit()
        return True

    """
       serialize for jsonify
    """
    def getSerializedCategories(self):
        categories = self.getCategories()
        return jsonify(Categories=\
                       [category.serialize for category in categories])

    def getSerializedItemsForCategory(self, category_id):
        items = self.getItemsForCategory(category_id)
        return jsonify(Items=[item.serialize for item in items])

    def getSerializedItem(self, item_id):
        item = self.getItemById(item_id)
        return jsonify(Item=[item.serialize])
