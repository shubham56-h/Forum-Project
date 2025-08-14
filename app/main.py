from flask import Blueprint, render_template, request, redirect, url_for, session
from .models import User
from . import db

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def login():
    return render_template('login.html', isVailid=True)

@main.route('/user', methods=['GET'])
def user():
    return render_template('user.html')

@main.route('/home', methods=['GET'])
def home():
    return render_template('index.html')

@main.route('/create_post', methods=["GET"])
def create_post():
    return render_template('create_post.html')

@main.route('/posts')
def posts():
    return render_template('posts.html')

@main.route('/edit/<int:id>', methods=['GET'])
def edit_post(id):
    return render_template('edit_post.html', postId=id)

@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))
