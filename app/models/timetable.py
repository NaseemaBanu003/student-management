from datetime import datetime, timezone

from app.extensions import db


class TimetableEntry(db.Model):
    __tablename__ = "timetable_entries"

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    room = db.Column(db.String(80), nullable=False)
    section = db.Column(db.String(20), default="A")
    academic_year_id = db.Column(db.Integer, db.ForeignKey("academic_years.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey("semesters.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id"), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    academic_year = db.relationship("AcademicYear", back_populates="timetables")
    course = db.relationship("Course", back_populates="timetables")
    semester = db.relationship("Semester", back_populates="timetables")
    subject = db.relationship("Subject", back_populates="timetables")
    faculty = db.relationship("Faculty", back_populates="timetable_entries")

    def __repr__(self):
        return f"<TimetableEntry {self.day}:{self.subject_id}>"
