from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.report import Report

reports_bp = Blueprint("reports", __name__)

@reports_bp.post("")
@jwt_required()
def submit_report():
    user_id = get_jwt_identity()
    data    = request.get_json()

    if not data or not data.get("content_type") or not data.get("content_id") or not data.get("reason"):
        return jsonify({"error": "content_type, content_id and reason are required"}), 400

    if data["content_type"] not in ("post", "comment"):
        return jsonify({"error": "content_type must be 'post' or 'comment'"}), 400

    # Prevent duplicate reports from same user
    existing = Report.query.filter_by(
        reporter_id  = user_id,
        content_type = data["content_type"],
        content_id   = data["content_id"],
        status       = "pending"
    ).first()
    if existing:
        return jsonify({"message": "Already reported"}), 200

    report = Report(
        reporter_id  = user_id,
        content_type = data["content_type"],
        content_id   = data["content_id"],
        reason       = data["reason"],
    )
    db.session.add(report)
    db.session.commit()

    return jsonify({"message": "Report submitted!", "report": report.to_dict()}), 201