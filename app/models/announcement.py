from datetime import datetime, timezone

from app.extensions import db


class Announcement(db.Model):
    __tablename__ = "announcements"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    audience = db.Column(db.String(40), default="everyone")
    target_department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=True)
    target_course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=True)
    target_semester_id = db.Column(db.Integer, db.ForeignKey("semesters.id"), nullable=True)
    target_section = db.Column(db.String(20), nullable=True)
    is_published = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime)
    scheduled_for = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    creator = db.relationship("User", foreign_keys=[created_by])

    def __repr__(self):
        return f"<Announcement {self.title}>"
