from datetime import datetime, timezone

from app.extensions import db


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), unique=True, nullable=False)
    admission_number = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    middle_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80), nullable=False)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(20))
    blood_group = db.Column(db.String(10))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    alternate_phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    city = db.Column(db.String(80))
    state = db.Column(db.String(80))
    pincode = db.Column(db.String(20))
    parent_name = db.Column(db.String(120))
    parent_phone = db.Column(db.String(20))
    parent_email = db.Column(db.String(120))
    emergency_contact = db.Column(db.String(20))
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    batch = db.Column(db.String(40))
    academic_year_id = db.Column(db.Integer, db.ForeignKey("academic_years.id"))
    semester_id = db.Column(db.Integer, db.ForeignKey("semesters.id"))
    section = db.Column(db.String(20), default="A")
    admission_date = db.Column(db.Date)
    status = db.Column(db.String(30), default="active")
    profile_photo = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, unique=True)

    user = db.relationship("User", back_populates="student")
    department = db.relationship("Department", back_populates="students")
    course = db.relationship("Course", back_populates="students")
    enrollments = db.relationship("StudentEnrollment", back_populates="student")
    attendance_records = db.relationship("Attendance", back_populates="student")
    marks = db.relationship("Mark", back_populates="student")
    fees = db.relationship("StudentFee", back_populates="student")
    payments = db.relationship("Payment", back_populates="student")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __repr__(self):
        return f"<Student {self.student_id}>"
