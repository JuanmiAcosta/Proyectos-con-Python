from flask import Flask

# export FLASK_APP=market.py
# export FLASK_DEBUG=1

# flask run

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Hello, World!</h1>'

@app.route('/about/<username>') #dynamic route
def about_page(username):
    return f'<h1>This is the about page of {username}</h1>'