from flask import request, redirect, url_for, render_template, flash
from flask import make_response
import jinja2, json, os, httplib2, random, string, requests
from functools import wraps
from flask import session as login_session
from flask_login import LoginManager, UserMixin, login_user, logout_user,\
                        current_user
from app import app
from authentication import *
from app.models import Category, Item
from app.main.database_operations import DatabaseOperations

lm = LoginManager(app)
lm.login_view = 'index'
@lm.user_loader
def load_user(id):
    return db.getUserById(int(id))

template_directory = os.path.join(os.getcwd(), 'templates')
jinja_environment = \
    jinja2.Environment(loader=jinja2.FileSystemLoader(template_directory),
                       autoescape=True)

db = DatabaseOperations()

def login_required(f):
    @wraps(f)
    def login_check(*args, **kwargs):
        if not current_user.is_anonymous:
            return f(*args, **kwargs)
        else:
            flash("You have to be logged in to access this page")
            return redirect('/login')
    return login_check


@app.route('/')
@app.route('/index')
def index():
    categories = db.getCategories()
    latest_items = db.getLatestItems(10)
    cat_items = {}
    for item in latest_items:
        cat_items[item.title] = db.getCategoryForItem(item)
    return render_template('index.html', categories=categories,
                            latest_items=latest_items, cat_items=cat_items)


@app.route('/category/<int:id>')
def showItems(id):
    category = db.getCategoryById(id=id)
    if not category:
        flash("The Category you requested does not exist")
        return redirect('/')
    itemCount = db.getNumberOfItemsPerCategory(category.id)
    items = db.getItemsForCategory(category.id)
    return render_template('items.html', category=category, items=items,
                            itemCount=itemCount)


@app.route('/category/item/<int:id>')
def item(id):
    item = db.getItemById(id=id)
    if not item:
        flash("Item you asked for does not exist.")
        return redirect('/')
    categoryName = db.getCategoryForItem(item)
    return render_template('item.html', item=item, categoryName=categoryName)


"""
   Routes for adding, updating and deleting items
   Also a route for signing in as user
   And a route for Logging in with third party oauth
"""
@app.route('/item/add', methods=['GET', 'POST'])
@login_required
def addItem():
    if request.method == 'GET':
        categories = db.getCategories()
        params = {}
        return render_template('newItem.html', categories=categories,
                                params=params)
    if request.method == 'POST':

        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')

        categories = db.getCategories()
        params = {'title': title, 'description': description,
                  'category': category}
        item = item_request(title, description, category, False)
        if item is None:
            return render_template('newItem.html', categories=categories,
                                    params=params)
        if db.addItem(item):
            flash("Item was added succesfully!")
            return redirect('/')
        else:
            flash("Something went wrong adding item.")
            return render_template('newItem.html', categories=categories,
                                    params=params)


def item_request(title, description, category, edit):
    """
       This is a helper method for both adding and
       editing an item, so there is no duplicate code.
    """
    creator_id = current_user.social_id
    categories = db.getCategories()
    params = {'title': title, 'description': description,
              'category': category}

    if not title:
        flash("A title is required.")
        return None

    if not description:
        flash("A description is required.")
        return None

    existingCategories = db.getExistingCategories()
    if not int(category) in existingCategories:
        flash("This is a non existing category.")
        return None

    # title must be unique in this category but not for editing.
    if not edit:
        titles = db.getCategoryTitles(category)
        if title in titles:
            flash("Existing title in this category: try another title.")
            return None

    if not creator_id:
        flash("Sorry, the session could not find logged in user.")
        return None

    item = Item(title, description, category, creator_id)
    return item


@app.route('/category/item/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def deleteItem(id):

    item = db.getItemById(id=id)
    creator = item.creator
    user_id = current_user.social_id

    if item.creator != user_id:
        flash("Sorry you have to be the creator of an item to delete it.")
        return redirect('/')
    if not item:
        flash('This item does not exist.')
        return redirect('/')

    if request.method == 'GET':
        return render_template('deleteItem.html', item=item)
    if request.method == 'POST':
        if request.form.get('action') != "Yes Delete":
            return redirect('/')
        user = current_user
        if db.deleteItem(item.id, user):
            flash("The item has been deleted succesfully.")
        else:
            flash("The item could not be deleted.")
        return redirect('/')


# you need to be logged in
@app.route('/item/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def editItem(id):
    item = db.getItemById(id=id)
    creator = db.getItemCreator(id=id)
    user_id = current_user.social_id

    params = {}
    if creator != user_id:
        flash("Sorry you need to be the creator of an item to edit it")
        return redirect('/')
    if not item:
        flash('This item does not exist')
        return redirect('/')

    if request.method == 'GET':
        # present a form for editing items
        categories = db.getCategories()
        return render_template('editItem.html', categories=categories,
                                params=params, item=item)

    if request.method == 'POST':

        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        categories = db.getCategories()

        params = {'title': title, 'description': description,
                  'category': category}

        new_item = item_request(title, description, category, True)

        if not new_item:
            flash("Item could not be updated.")
            return render_template('editItem.html', categories=categories,
                                    params=params, item=item)

        if db.updateItem(item.id, new_item, current_user):
            flash("Succesfully edited item.")
            return redirect('/')
        return render_template('editItem.html', categories=categories,
                                params=params, item=item)


@app.route('/categories.json/')
def categoriesJson():
    categories = db.getSerializedCategories()
    return categories


@app.route('/category/<int:id>/items.json/')
def itemsJson(id):
    items = db.getSerializedItemsForCategory(id)
    return items


@app.route('/category/item/<int:id>/item.json/')
def itemJson(id):
    item = db.getSerializedItem(id)
    return item


@app.route('/login')
def login():
    # Create anti-forgery state token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)\
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = db.getUserBySocialId(social_id=social_id)
    if not user:
        user = db.addUser(social_id=social_id, name=username, email=email)
    login_user(user, True)
    flash('logged in with: ' + provider + ' as ' + username)
    return redirect(url_for('index'))
