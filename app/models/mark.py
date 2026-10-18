from datetime import datetime, timezone

from app.extensions import db


class Mark(db.Model):
    __tablename__ = "marks"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey("exams.id"), nullable=False)
    maximum_marks = db.Column(db.Float, default=100.0)
    marks_obtained = db.Column(db.Float, default=0.0)
    grade = db.Column(db.String(10))
    grade_point = db.Column(db.Float, default=0.0)
    remarks = db.Column(db.Text)
    is_published = db.Column(db.Boolean, default=False)
    is_locked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    student = db.relationship("Student", back_populates="marks")
    subject = db.relationship("Subject", back_populates="marks")
    exam = db.relationship("Exam", back_populates="marks")

    def __repr__(self):
        return f"<Mark {self.student_id}:{self.subject_id}:{self.grade}>"
