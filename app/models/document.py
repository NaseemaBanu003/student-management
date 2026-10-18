from datetime import datetime, timezone

from app.extensions import db


class Document(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    content_type = db.Column(db.String(120), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    storage_path = db.Column(db.String(255), nullable=False)
    document_type = db.Column(db.String(60), default="general")
    uploaded_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    uploader = db.relationship("User", foreign_keys=[uploaded_by])

    def __repr__(self):
        return f"<Document {self.title}>"
