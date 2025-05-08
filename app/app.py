from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__,
            static_folder='../static',
            template_folder='templates')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-123')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///plottwist.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    from .databse import User
    return User.query,get(int(user_id))

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
