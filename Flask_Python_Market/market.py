from flask import Flask, render_template

# export FLASK_APP=market.py
# export FLASK_DEBUG=1

# flask run

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market')
def market_page():
    items = [ #lista de diccionarios
        {'id': 1, 'name': 'Meta Quest 3', 'barcode': '893212299897', 'price': 400},
        {'id': 2, 'name': 'Asus Tuf Gaming A15 2023', 'barcode': '123985473165', 'price': 1300},
        {'id': 3, 'name': 'Samsung Tab S7', 'barcode': '231985128446', 'price': 700},
    ]
    return render_template('market.html', items = items)


@app.route('/about/<username>')  # dynamic route
def about_page(username):
    return f'<h1>This is the about page of {username}</h1>'
