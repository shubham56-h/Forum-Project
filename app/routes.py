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

@main.route('/create_post', methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        content = request.form.get('content')
        tags = request.form.get('tags')
        user_id = session.get('user_id')
        new_post = Post(title=title, content=content, category=category, tags=tags, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('main.posts'))

    return render_template('create_post.html')

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

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post_to_edit = Post.query.get_or_404(id)
    # user_id = session.get('user_id')

    # if post_to_edit.user_id != user_id:
    #     abort(403)

    if request.method == 'POST':
        post_to_edit.title = request.form.get('title')
        post_to_edit.content = request.form.get('content')
        post_to_edit.category = request.form.get('category')
        post_to_edit.tags = request.form.get('post_tags', '')
        post_to_edit.allow_comments = True if request.form.get('allow_comments') else False
        post_to_edit.updated_at = datetime.utcnow()  # Update the timestamp
        
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.posts'))

    return render_template('edit_post.html', post=post_to_edit)

@main.route('/delete/<int:id>', methods=['GET','POST'])
@login_required
def delete_post(id):
    post_to_delete = Post.query.get(id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('main.posts'))

@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))
