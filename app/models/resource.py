from app import db
from datetime import datetime, timezone

class Resource(db.Model):
    __tablename__ = "resources"

    id          = db.Column(db.Integer, primary_key=True)
    author_id   = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    url         = db.Column(db.String(500), nullable=True)
    category    = db.Column(db.String(30), nullable=False, default="other")
    is_active   = db.Column(db.Boolean, default=True)
    created_at  = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    author = db.relationship("User", backref="resources")

    def to_dict(self):
        # Returns active resources to the frontend
        return {
            "id":          self.id,
            "title":       self.title,
            "description": self.description,
            "url":         self.url,
            "category":    self.category,
            "created_at":  self.created_at.isoformat(),
        }