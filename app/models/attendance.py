from datetime import datetime, timezone

from app.extensions import db


class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.id"), nullable=False)
    attendance_date = db.Column(db.Date, nullable=False)
    period = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    student = db.relationship("Student", back_populates="attendance_records")
    subject = db.relationship("Subject", back_populates="attendance_records")
    faculty = db.relationship("Faculty", back_populates="attendance_records")

    __table_args__ = (
        db.UniqueConstraint("student_id", "subject_id", "attendance_date", "period", name="uq_student_subject_date_period"),
    )

    def __repr__(self):
        return f"<Attendance {self.student_id}:{self.subject_id}:{self.attendance_date}>"
