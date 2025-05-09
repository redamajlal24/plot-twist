from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config

load_dotenv()

app = Flask(__name__,
            static_folder='../static',
            template_folder='templates')

env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    from .database import User
    return User.query.get(int(user_id))

@app.route('/')
def home():
    lang = request.args.get('lang', default=0, type=int)
    return render_template('home.html', lang=lang)

@app.route('/about')
def about():
    lang = request.args.get('lang', default=0, type=int)
    return render_template('about.html', lang=lang)

@app.route('/contact')
def contact():
    lang = request.args.get('lang', default=0, type=int)
    return render_template('contact.html', lang=lang)

if __name__ == '__main__':
    app.run(debug=True)
