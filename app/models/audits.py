from datetime import datetime, timezone

from app.extensions import db


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    action = db.Column(db.String(120), nullable=False)
    entity = db.Column(db.String(120), nullable=False)
    entity_id = db.Column(db.Integer)
    ip_address = db.Column(db.String(60))
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship("User", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog {self.action}:{self.entity}>"
