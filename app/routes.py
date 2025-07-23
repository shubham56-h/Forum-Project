from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Post
from . import db

main = Blueprint('main', __name__)

def is_logged_in():
    return session.get('user_id') is not None

@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
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
def home():
    if not is_logged_in():
        return redirect(url_for('main.login'))

    return render_template('index.html', posted=False)

@main.route('/create_post', methods=["GET", "POST"])
def create_post():
    if not is_logged_in():
        return redirect(url_for('main.login'))
    
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
def posts():
    if not is_logged_in():
        return redirect(url_for('main.login'))

    all_posts = Post.query.all()
    return render_template('posts.html', posts=all_posts, user=user)

@main.route('/delete/<int:id>', methods=['POST'])
def delete_post(id):
    if not is_logged_in():
        return redirect(url_for('main.login'))

    post_to_delete = Post.query.get_or_404(id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('main.posts'))

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    if not is_logged_in():
        return redirect(url_for('main.login'))

    post_to_edit = Post.query.get_or_404(id)

    if request.method == 'POST':
        post_to_edit.title = request.form.get('title')
        post_to_edit.desc = request.form.get('desc')
        db.session.commit()
        return redirect(url_for('main.posts'))

    return render_template('index.html', post=post_to_edit)

@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))
