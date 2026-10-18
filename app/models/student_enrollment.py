from datetime import datetime, timezone

from app.extensions import db


class StudentEnrollment(db.Model):
    __tablename__ = "student_enrollments"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    academic_year_id = db.Column(db.Integer, db.ForeignKey("academic_years.id"), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey("semesters.id"), nullable=False)
    section = db.Column(db.String(20), default="A")
    enrollment_status = db.Column(db.String(30), default="active")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    student = db.relationship("Student", back_populates="enrollments")
    department = db.relationship("Department", back_populates="enrollments")
    course = db.relationship("Course", back_populates="enrollments")
    academic_year = db.relationship("AcademicYear", back_populates="enrollments")
    semester = db.relationship("Semester", back_populates="enrollments")

    def __repr__(self):
        return f"<StudentEnrollment {self.student_id}:{self.academic_year_id}>"
