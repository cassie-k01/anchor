from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from app import db
from app.models.report import Report
from app.models.post import Post
from app.models.comment import Comment
from app.models.user import User

admin_bp = Blueprint("admin", __name__)

# Decorator that blocks anyone who isn't a moderator or admin
def moderator_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user    = User.query.get(user_id)
        if not user or user.role not in ("moderator", "admin"):
            return jsonify({"error": "Moderator access required"}), 403
        return fn(*args, **kwargs)
    return wrapper


@admin_bp.get("/reports")
@moderator_required
def list_reports():
    status  = request.args.get("status", "pending")
    reports = Report.query.filter_by(status=status).order_by(Report.created_at.desc()).all()
    return jsonify({"reports": [r.to_dict() for r in reports]}), 200


@admin_bp.patch("/reports/<int:report_id>")
@moderator_required
def update_report(report_id):
    user_id = get_jwt_identity()
    data    = request.get_json()
    report  = Report.query.get(report_id)

    if not report:
        return jsonify({"error": "Report not found"}), 404

    if data.get("status") not in ("pending", "reviewed", "resolved"):
        return jsonify({"error": "Invalid status"}), 400

    report.status      = data["status"]
    report.reviewed_by = user_id
    db.session.commit()

    return jsonify({"message": "Report updated!", "report": report.to_dict()}), 200


@admin_bp.delete("/content/<content_type>/<int:content_id>")
@moderator_required
def remove_content(content_type, content_id):
    # Handles both post and comment removal through one route
    if content_type == "post":
        item = Post.query.get(content_id)
    elif content_type == "comment":
        item = Comment.query.get(content_id)
    else:
        return jsonify({"error": "Invalid content type"}), 400

    if not item:
        return jsonify({"error": "Content not found"}), 404

    # Applies a soft delete
    item.status = "removed"
    db.session.commit()
    return jsonify({"message": f"{content_type.capitalize()} removed!"}), 200


@admin_bp.patch("/users/<int:user_id>/suspend")
@moderator_required
def suspend_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Setting is_active to False prevents the user from logging in
    user.is_active = False
    db.session.commit()
    return jsonify({"message": "User suspended"}), 200