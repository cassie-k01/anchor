from app import db
from datetime import datetime, timezone

class Comment(db.Model):
    __tablename__ = "comments"

    id                = db.Column(db.Integer, primary_key=True)
    post_id           = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    author_id         = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    alias             = db.Column(db.String(60), nullable=False)
    parent_comment_id = db.Column(db.Integer, db.ForeignKey("comments.id"), nullable=True)
    body              = db.Column(db.Text, nullable=False)
    is_anonymous      = db.Column(db.Boolean, default=True)
    status            = db.Column(db.String(20), default="active")
    created_at        = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    author  = db.relationship("User", backref="comments")
    post    = db.relationship("Post", backref="comments")
    replies = db.relationship("Comment", backref=db.backref("parent", remote_side="Comment.id"))

    def to_dict(self):
        if self.is_anonymous:
            author_display = self.alias
        else:
            author_display = self.author.display_name

        return {
            "id":                self.id,
            "post_id":           self.post_id,
            "parent_comment_id": self.parent_comment_id,
            "body":              self.body,
            "is_anonymous":      self.is_anonymous,
            "author":            author_display,
            "created_at":        self.created_at.isoformat(),
            "replies":           [r.to_dict() for r in self.replies if r.status == "active"],
        }