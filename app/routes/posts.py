from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.post import Post, VALID_CATEGORIES
from app.models.user import User
import random

posts_bp = Blueprint("posts", __name__)

# Simple alias generator
ADJECTIVES = ["Tranquil", "Brave", "Quiet", "Bold", "Calm", "Gentle", "Swift", "Bright"]
NOUNS      = ["River", "Mountain", "Dawn", "Forest", "Ocean", "Star", "Breeze", "Ember"]

def get_or_create_alias(user_id):
    """Every user gets one consistent alias across all their anonymous posts."""
    # Use user_id as seed so same user always gets same alias
    random.seed(user_id)
    alias = random.choice(ADJECTIVES) + random.choice(NOUNS) + str(random.randint(10, 99))
    return alias


@posts_bp.get("")
@jwt_required()
def get_posts():
    # category filter and pagination from query params
    category = request.args.get("category")
    page     = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 20))

    query = Post.query.filter_by(status="active").order_by(Post.created_at.desc())

    if category and category in VALID_CATEGORIES:
        query = query.filter_by(category=category)

    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "posts": [p.to_dict() for p in paginated.items],
        "total": paginated.total,
        "page":  page,
        "pages": paginated.pages,
    }), 200


@posts_bp.post("")
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
    user    = User.query.get(user_id)
    data    = request.get_json()

    if not data or not data.get("title") or not data.get("body"):
        return jsonify({"error": "Title and body are required"}), 400

    category = data.get("category", "other")
    if category not in VALID_CATEGORIES:
        return jsonify({"error": f"Category must be one of: {', '.join(VALID_CATEGORIES)}"}), 400

    is_anonymous = data.get("is_anonymous", True)

    # Use alias if anonymous,real name if not
    
    alias        = get_or_create_alias(user_id) if is_anonymous else user.display_name

    post = Post(
        author_id    = user_id,
        alias        = alias,
        title        = data["title"],
        body         = data["body"],
        category     = category,
        is_anonymous = is_anonymous,
    )
    db.session.add(post)
    db.session.commit()

    return jsonify({"message": "Post created!", "post": post.to_dict()}), 201


@posts_bp.get("/<int:post_id>")
@jwt_required()
def get_post(post_id):
    post = Post.query.get(post_id)
    if not post or post.status == "removed":
        return jsonify({"error": "Post not found"}), 404

    # Track how many times a post has been viewed
    post.view_count += 1
    db.session.commit()

    return jsonify(post.to_dict()), 200


@posts_bp.delete("/<int:post_id>")
@jwt_required()
def delete_post(post_id):
    user_id = get_jwt_identity()
    user    = User.query.get(user_id)
    post    = Post.query.get(post_id)

    if not post:
        return jsonify({"error": "Post not found"}), 404
   
    # Only the author / moderator can delete a post
    
    if str(post.author_id) != str(user_id) and user.role not in ("moderator", "admin"):
        return jsonify({"error": "Unauthorized"}), 403
    # Soft delete which keeps the record in the database but hides it from the feed
    post.status = "removed"
    db.session.commit()
    return jsonify({"message": "Post removed"}), 200