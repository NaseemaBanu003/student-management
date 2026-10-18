from datetime import datetime, timezone

from app.extensions import db


class Semester(db.Model):
    __tablename__ = "semesters"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    subjects = db.relationship("Subject", back_populates="semester")
    enrollments = db.relationship("StudentEnrollment", back_populates="semester")
    exams = db.relationship("Exam", back_populates="semester")
    timetables = db.relationship("TimetableEntry", back_populates="semester")

    def __repr__(self):
        return f"<Semester {self.name}>"
