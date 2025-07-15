from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Post
from . import db

main = Blueprint('main', __name__)

def is_logged_in():
    return 'user_id' in session

@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = username
            return redirect(url_for('main.home'))
        return render_template('login.html', isVailid=False)
    
    return render_template('login.html', isVailid=True)

@main.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
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

    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        new_post = Post(title=title, desc=desc)
        db.session.add(new_post)
        db.session.commit()
        return render_template('index.html', posted=True)

    return render_template('index.html', posted=False)

@main.route('/posts')
def posts():
    if not is_logged_in():
        return redirect(url_for('main.login'))

    all_posts = Post.query.all()
    return render_template('posts.html', posts=all_posts)

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
