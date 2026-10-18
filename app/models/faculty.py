from datetime import datetime, timezone

from app.extensions import db


class Faculty(db.Model):
    __tablename__ = "faculty"

    id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.String(50), unique=True, nullable=False)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    qualification = db.Column(db.String(120))
    specialization = db.Column(db.String(120))
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    designation = db.Column(db.String(80), default="Lecturer")
    joining_date = db.Column(db.Date)
    experience = db.Column(db.Integer, default=0)
    status = db.Column(db.String(30), default="active")
    profile_photo = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, unique=True)

    user = db.relationship("User", back_populates="faculty")
    department = db.relationship("Department", back_populates="faculty")
    faculty_subjects = db.relationship("FacultySubject", back_populates="faculty")
    timetable_entries = db.relationship("TimetableEntry", back_populates="faculty")
    attendance_records = db.relationship("Attendance", back_populates="faculty")
    exams = db.relationship("Exam", back_populates="faculty")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __repr__(self):
        return f"<Faculty {self.faculty_id}>"
