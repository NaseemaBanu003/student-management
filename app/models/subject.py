from datetime import datetime, timezone

from app.extensions import db


class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(40), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    credits = db.Column(db.Integer, nullable=False, default=4)
    subject_type = db.Column(db.String(40), default="Theory")
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey("semesters.id"), nullable=False)
    status = db.Column(db.String(30), default="active")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    department = db.relationship("Department", back_populates="subjects")
    course = db.relationship("Course", back_populates="subjects")
    semester = db.relationship("Semester", back_populates="subjects")
    faculty_assignments = db.relationship("FacultySubject", back_populates="subject")
    attendance_records = db.relationship("Attendance", back_populates="subject")
    marks = db.relationship("Mark", back_populates="subject")
    exams = db.relationship("Exam", back_populates="subject")
    timetables = db.relationship("TimetableEntry", back_populates="subject")

    def __repr__(self):
        return f"<Subject {self.code}>"
