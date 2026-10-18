from datetime import datetime, timezone

from app.extensions import db


class FacultySubject(db.Model):
    __tablename__ = "faculty_subjects"

    id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    academic_year_id = db.Column(db.Integer, db.ForeignKey("academic_years.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    faculty = db.relationship("Faculty", back_populates="faculty_subjects")
    subject = db.relationship("Subject", back_populates="faculty_assignments")
    academic_year = db.relationship("AcademicYear", back_populates="faculty_subjects")

    def __repr__(self):
        return f"<FacultySubject {self.faculty_id}:{self.subject_id}>"
