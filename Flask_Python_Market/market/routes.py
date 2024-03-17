from market import app
from flask import render_template
from market.models import Item

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market')
def market_page():
    items = Item.query.all() # query from market.db
    return render_template('market.html', items=items)


@app.route('/about/<username>')  # dynamic route
def about_page(username):
    return f'<h1>This is the about page of {username}</h1>'