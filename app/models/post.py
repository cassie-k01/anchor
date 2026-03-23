from app import db
from datetime import datetime, timezone

VALID_CATEGORIES = ("academics", "relationships", "career", "wellness", "other")

class Post(db.Model):
    __tablename__ = "posts"

    id           = db.Column(db.Integer, primary_key=True)
    author_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    alias        = db.Column(db.String(60), nullable=False)
    title        = db.Column(db.String(200), nullable=False)
    body         = db.Column(db.Text, nullable=False)
    category     = db.Column(db.String(30), nullable=False, default="other")
    is_anonymous = db.Column(db.Boolean, default=True)
    status       = db.Column(db.String(20), default="active")
    view_count   = db.Column(db.Integer, default=0)
    created_at   = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Link back to the user who wrote it
    author = db.relationship("User", backref="posts")

    def to_dict(self):
        # Show alias if anonymous, real name if not
        if self.is_anonymous:
            author_display = self.alias
        else:
            author_display = self.author.display_name

        return {
            "id":           self.id,
            "title":        self.title,
            "body":         self.body,
            "category":     self.category,
            "is_anonymous": self.is_anonymous,
            "author":       author_display,  # never exposes real identity
            "view_count":   self.view_count,
            "created_at":   self.created_at.isoformat(),
        }