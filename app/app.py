from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
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

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('signup'))
            
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('login'))
        
    lang = request.args.get('lang', default=0, type=int)
    return render_template('signup.html', lang=lang)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter((User.username == username) | (User.email == username)).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        
        flash('Invalid username or password')
        return redirect(url_for('login'))
        
    lang = request.args.get('lang', default=0, type=int)
    return render_template('login.html', lang=lang)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
