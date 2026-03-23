from app import db
from datetime import datetime, timezone

class User(db.Model):
    __tablename__ = "users"

    id            = db.Column(db.Integer, primary_key=True)
    email         = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    display_name  = db.Column(db.String(100), nullable=False)
    academic_year = db.Column(db.Integer, nullable=False)
    role          = db.Column(db.String(20), default="student")
    is_active     = db.Column(db.Boolean, default=True)
    created_at    = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        # Returns user info,always excluding the password hash
        return {
            "id":            self.id,
            "email":         self.email,
            "display_name":  self.display_name,
            "academic_year": self.academic_year,
            "role":          self.role,
        }