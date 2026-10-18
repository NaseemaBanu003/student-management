from datetime import datetime, timezone

from app.extensions import db


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(40), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    degree_type = db.Column(db.String(80), nullable=False)
    duration = db.Column(db.Integer, nullable=False, default=4)
    total_semesters = db.Column(db.Integer, nullable=False, default=8)
    description = db.Column(db.Text)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    status = db.Column(db.String(30), default="active")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    department = db.relationship("Department", back_populates="courses")
    students = db.relationship("Student", back_populates="course")
    subjects = db.relationship("Subject", back_populates="course")
    enrollments = db.relationship("StudentEnrollment", back_populates="course")
    exams = db.relationship("Exam", back_populates="course")
    timetables = db.relationship("TimetableEntry", back_populates="course")

    def __repr__(self):
        return f"<Course {self.code}>"
