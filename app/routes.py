from datetime import datetime
from flask import Blueprint, abort, flash, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Post
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

@main.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('index.html', posted=False)

@main.route('/create_post', methods=["GET"])
@login_required
def create_post():
    return render_template('create_post.html')

@main.route('/api/create_post', methods=['POST'])
@login_required
def api_create_post():
    data = request.get_json()
    user_id = session.get('user_id')

    new_post = Post(
        title = data['title'],
        category = data['category'],
        content = data['content'],
        tags = data['tags'],
        user_id = user_id
    )
    db.session.add(new_post)
    db.session.commit()

    return {'message' : 'posted successfully'}, 200

@main.route('/posts')
@login_required
def posts():
    return render_template('posts.html')

@main.route('/api/posts', methods=['GET'])
@login_required
def api_get_posts():
    posts = Post.query.all()
    post_list = []

    for post in posts:
        post_list.append({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'category': post.category,
            'tags': post.tags,
            'user_id': post.user_id
        })

    return {'posts': post_list}, 200  # Return JSON response

@main.route('/edit/<int:id>', methods=['GET'])
@login_required
def edit_post(id):
    post_to_edit = Post.query.get_or_404(id)
    # user_id = session.get('user_id')

    # if post_to_edit.user_id != user_id:
    #     abort(403)
    return render_template('edit_post.html', post=post_to_edit)

@main.route('/api/posts/<int:id>', methods=['DELETE'])
@login_required
def api_delete_post(id):
    post_to_delete = Post.query.get(id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return {'message' : 'deleted successfully'}, 200

@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))
