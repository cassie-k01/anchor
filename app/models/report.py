from app import db
from datetime import datetime, timezone

class Report(db.Model):
    __tablename__ = "reports"

    id           = db.Column(db.Integer, primary_key=True)
    reporter_id  = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content_type = db.Column(db.String(20), nullable=False)  # 'post' or 'comment'
    content_id   = db.Column(db.Integer, nullable=False)
    reason       = db.Column(db.String(300), nullable=False)
    status       = db.Column(db.String(20), default="pending")
    reviewed_by  = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at   = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    reporter = db.relationship("User", foreign_keys=[reporter_id], backref="reports")
    reviewer = db.relationship("User", foreign_keys=[reviewed_by])

    def to_dict(self):
        return {
            "id":           self.id,
            "reporter_id":  self.reporter_id,
            "content_type": self.content_type,
            "content_id":   self.content_id,
            "reason":       self.reason,
            "status":       self.status,
            "created_at":   self.created_at.isoformat(),
        }