from flask import Blueprint, redirect, request, jsonify, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Post
from . import db
from sqlalchemy.exc import IntegrityError
from .models import User
from .main import login_required  # Import the decorator from main

api = Blueprint('api', __name__)

@api.route('/user', methods=['POST'])
def create_user():
    try:
        # Parse JSON body instead of form data (modern APIs prefer JSON)
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid or missing JSON body"}), 400

        # Extract and validate fields
        required_fields = ["fullname", "username", "password", "email"]
        missing_fields = [f for f in required_fields if not data.get(f)]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        # Hash password
        hashed_pass = generate_password_hash(data["password"])

        # Create user instance
        new_user = User(
            full_name=data["fullname"].strip(),
            username=data["username"].strip(),
            password=hashed_pass,
            email=data["email"].strip().lower()
        )

        # Save to DB
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "User created successfully",
            "user": {
                "id": new_user.id,
                "fullname": new_user.full_name,
                "username": new_user.username,
                "email": new_user.email
            }
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username or email already exists"}), 409

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password are required"}), 400

    email = data["email"].strip().lower()
    password = data["password"]

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401
    
    session.permanent = True
    session['user_id'] = user.id

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "fullname": user.full_name,
            "username": user.username,
            "email": user.email
        }
    }), 200


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