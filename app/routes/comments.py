from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User
from app.routes.posts import get_or_create_alias

comments_bp = Blueprint("comments", __name__)


@comments_bp.get("/posts/<int:post_id>/comments")
@jwt_required()
def get_comments(post_id):
    post = Post.query.get(post_id)
    if not post or post.status == "removed":
        return jsonify({"error": "Post not found"}), 404

    # Only return top level comments, replies are nested inside each
    top_level = Comment.query.filter_by(
        post_id=post_id,
        parent_comment_id=None,
        status="active"
    ).order_by(Comment.created_at.asc()).all()

    return jsonify({"comments": [c.to_dict() for c in top_level]}), 200


@comments_bp.post("/posts/<int:post_id>/comments")
@jwt_required()
def add_comment(post_id):
    user_id = get_jwt_identity()
    user    = User.query.get(user_id)
    data    = request.get_json()

    post = Post.query.get(post_id)
    if not post or post.status == "removed":
        return jsonify({"error": "Post not found"}), 404

    if not data or not data.get("body"):
        return jsonify({"error": "Comment body is required"}), 400

    # Check if this is a reply to another comment
    parent_id = data.get("parent_comment_id")
    if parent_id:
        parent = Comment.query.get(parent_id)
        if not parent or parent.post_id != post_id:
            return jsonify({"error": "Invalid parent comment"}), 400

    is_anonymous = data.get("is_anonymous", True)
    alias        = get_or_create_alias(user_id) if is_anonymous else user.display_name

    comment = Comment(
        post_id           = post_id,
        author_id         = user_id,
        alias             = alias,
        parent_comment_id = parent_id,
        body              = data["body"],
        is_anonymous      = is_anonymous,
    )
    db.session.add(comment)
    db.session.commit()

    return jsonify({"message": "Comment added!", "comment": comment.to_dict()}), 201


@comments_bp.delete("/comments/<int:comment_id>")
@jwt_required()
def delete_comment(comment_id):
    user_id = get_jwt_identity()
    user    = User.query.get(user_id)
    comment = Comment.query.get(comment_id)

    if not comment:
        return jsonify({"error": "Comment not found"}), 404
    # Only the author / moderator can delete a comment
    if str(comment.author_id) != str(user_id) and user.role not in ("moderator", "admin"):
        return jsonify({"error": "Unauthorized"}), 403
    # Applies a soft delete
    comment.status = "removed"
    db.session.commit()
    return jsonify({"message": "Comment removed"}), 200