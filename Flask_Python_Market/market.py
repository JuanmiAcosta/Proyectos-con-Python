from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# export FLASK_APP=market.py
# export FLASK_ENV=development
# export FLASK_DEBUG=1

# flask run

# source .venv/bin/activate

# pip install flask-sqlalchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db' #añadiendo configuración
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)

    def __repr__(self):
        return f'Item{self.name}'


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
