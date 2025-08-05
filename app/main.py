from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from functools import wraps

main = Blueprint('main', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session.permanent=True
            session['user_id'] = user.id
            return redirect(url_for('main.home'))
        return render_template('login.html', isVailid=False)
    
    return render_template('login.html', isVailid=True)

@main.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        full_name = request.form.get('fullname')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        hashed_pass = generate_password_hash(password)

        new_user = User(full_name=full_name, username=username, password=hashed_pass, email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.login'))
    
    return render_template('user.html')

@main.route('/home', methods=['GET'])
@login_required
def home():
    return render_template('index.html')

@main.route('/create_post', methods=["GET"])
@login_required
def create_post():
    return render_template('create_post.html')

@main.route('/posts')
@login_required
def posts():
    return render_template('posts.html')

@main.route('/edit/<int:id>', methods=['GET'])
@login_required
def edit_post(id):
    return render_template('edit_post.html', postId=id)

@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))
