from flask import Blueprint, request, jsonify, session
from .models import Post
from . import db
from .main import login_required  # Import the decorator from main

api = Blueprint('api', __name__)

@api.route('/posts', methods=['POST'])
@login_required
def create_post():
    data = request.get_json()
    user_id = session.get('user_id')

    new_post = Post(
        title=data['title'],
        category=data['category'],
        content=data['content'],
        tags=data['tags'],
        user_id=user_id
    )
    db.session.add(new_post)
    db.session.commit()

    return jsonify({'message': 'posted successfully'}), 200

@api.route('/posts', methods=['GET'])
@login_required
def get_posts():
    posts = Post.query.all()
    post_list = [{
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'category': post.category,
        'tags': post.tags,
        'user_id': post.user_id
    } for post in posts]

    return jsonify({'posts': post_list}), 200

@api.route('/posts/<int:id>', methods=['GET'])
@login_required
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'category': post.category,
        'tags': post.tags,
        'user_id': post.user_id
    }), 200

@api.route('/posts/<int:id>', methods=['PUT'])
@login_required
def edit_post(id):
    post_to_edit = Post.query.get_or_404(id)
    data = request.get_json()

    post_to_edit.title = data['title']
    post_to_edit.category = data['category']
    post_to_edit.content = data['content']
    post_to_edit.tags = data['tags']
    db.session.commit()
    
    return jsonify({"message": "Edited successfully"}), 200

@api.route('/posts/<int:id>', methods=['DELETE'])
@login_required
def delete_post(id):
    post_to_delete = Post.query.get_or_404(id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return jsonify({'message': 'deleted successfully'}), 200