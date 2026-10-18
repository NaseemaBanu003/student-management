from datetime import datetime, timezone

from app.extensions import db


class AcademicYear(db.Model):
    __tablename__ = "academic_years"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    enrollments = db.relationship("StudentEnrollment", back_populates="academic_year")
    timetables = db.relationship("TimetableEntry", back_populates="academic_year")
    faculty_subjects = db.relationship("FacultySubject", back_populates="academic_year")

    def __repr__(self):
        return f"<AcademicYear {self.name}>"
