from datetime import datetime, timezone

from app.extensions import db


class Exam(db.Model):
    __tablename__ = "exams"

    id = db.Column(db.Integer, primary_key=True)
    exam_name = db.Column(db.String(120), nullable=False)
    exam_type = db.Column(db.String(40), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey("semesters.id"), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id"), nullable=True)
    exam_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    room = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    subject = db.relationship("Subject", back_populates="exams")
    course = db.relationship("Course", back_populates="exams")
    semester = db.relationship("Semester", back_populates="exams")
    faculty = db.relationship("Faculty", back_populates="exams")
    marks = db.relationship("Mark", back_populates="exam")

    def __repr__(self):
        return f"<Exam {self.exam_name}>"
