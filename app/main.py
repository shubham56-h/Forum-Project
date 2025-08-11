from flask import Blueprint, render_template, request, redirect, url_for, session
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
    return render_template('login.html', isVailid=True)

@main.route('/user', methods=['GET'])
def user():
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
