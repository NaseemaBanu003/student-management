from datetime import datetime, timezone

from app.extensions import db


class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    code = db.Column(db.String(30), nullable=False, unique=True)
    description = db.Column(db.Text)
    head_name = db.Column(db.String(120))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    courses = db.relationship("Course", back_populates="department")
    students = db.relationship("Student", back_populates="department")
    faculty = db.relationship("Faculty", back_populates="department")
    subjects = db.relationship("Subject", back_populates="department")
    enrollments = db.relationship("StudentEnrollment", back_populates="department")

    def __repr__(self):
        return f"<Department {self.name}>"
