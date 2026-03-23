from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.resource import Resource
from app.models.user import User

resources_bp = Blueprint("resources", __name__)


@resources_bp.get("")
@jwt_required()
def list_resources():
    category = request.args.get("category")
    query    = Resource.query.filter_by(is_active=True).order_by(Resource.created_at.desc())

    if category:
        query = query.filter_by(category=category)

    return jsonify({"resources": [r.to_dict() for r in query.all()]}), 200


@resources_bp.post("")
@jwt_required()
def create_resource():
    user_id = get_jwt_identity()
    user    = User.query.get(user_id)

    if user.role not in ("mentor", "moderator", "admin"):
        return jsonify({"error": "Only mentors and admins can add resources"}), 403

    data = request.get_json()
    if not data or not data.get("title") or not data.get("description"):
        return jsonify({"error": "Title and description are required"}), 400

    resource = Resource(
        author_id   = user_id,
        title       = data["title"],
        description = data["description"],
        url         = data.get("url"),
        category    = data.get("category", "other"),
    )
    db.session.add(resource)
    db.session.commit()

    return jsonify({"message": "Resource added!", "resource": resource.to_dict()}), 201


@resources_bp.delete("/<int:resource_id>")
@jwt_required()
def delete_resource(resource_id):
    user_id  = get_jwt_identity()
    user     = User.query.get(user_id)
    resource = Resource.query.get(resource_id)

    if not resource:
        return jsonify({"error": "Resource not found"}), 404

    if user.role not in ("mentor", "moderator", "admin"):
        return jsonify({"error": "Unauthorized"}), 403

    resource.is_active = False
    db.session.commit()
    return jsonify({"message": "Resource removed!"}), 200