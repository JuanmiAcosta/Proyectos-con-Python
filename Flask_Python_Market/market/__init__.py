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

from market import routes
