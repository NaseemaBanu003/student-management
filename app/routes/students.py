from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Student, Department, Course, AcademicYear, Semester, StudentEnrollment
from app.routes.auth import get_current_user, role_required

students_bp = Blueprint("students", __name__)


@students_bp.route("/students", methods=["GET"])
@jwt_required()
def list_students():
    students = Student.query.order_by(Student.id.desc()).paginate(page=1, per_page=20, error_out=False)
    payload = [{"id": s.id, "student_id": s.student_id, "full_name": s.full_name, "email": s.email, "status": s.status} for s in students.items]
    return {"success": True, "data": payload, "pagination": {"page": students.page, "pages": students.pages, "total": students.total}}, 200


@students_bp.route("/students", methods=["POST"])
@jwt_required()
@role_required("super_admin", "admin")
def create_student():
    data = request.get_json(silent=True) or {}
    required = ["first_name", "last_name", "email", "department_id", "course_id"]
    missing = [field for field in required if not data.get(field)]
    if missing:
        return {"success": False, "message": "Missing required fields", "errors": missing}, 400
    department = db.session.get(Department, data["department_id"])
    course = db.session.get(Course, data["course_id"])
    if not department or not course:
        return {"success": False, "message": "Invalid department or course"}, 400

    student = Student(
        student_id=f"STU-{Student.query.count() + 1:04d}",
        admission_number=f"ADM-{Student.query.count() + 1:05d}",
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        phone=data.get("phone", ""),
        department_id=department.id,
        course_id=course.id,
        batch=data.get("batch", "2026"),
        status=data.get("status", "active"),
        is_active=True,
    )
    db.session.add(student)
    db.session.flush()

    if data.get("academic_year_id") and data.get("semester_id"):
        db.session.add(
            StudentEnrollment(
                student_id=student.id,
                department_id=department.id,
                course_id=course.id,
                academic_year_id=data["academic_year_id"],
                semester_id=data["semester_id"],
                section=data.get("section", "A"),
            )
        )

    db.session.commit()
    return {"success": True, "message": "Student created successfully", "data": {"id": student.id}}, 201


@students_bp.route("/students/<int:student_id>", methods=["GET"])
@jwt_required()
def get_student(student_id):
    student = Student.query.get_or_404(student_id)
    return {"success": True, "data": {"id": student.id, "student_id": student.student_id, "full_name": student.full_name, "email": student.email, "status": student.status}}, 200


@students_bp.route("/students/<int:student_id>", methods=["PUT"])
@jwt_required()
@role_required("super_admin", "admin")
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    payload = request.get_json(silent=True) or {}
    for key, value in payload.items():
        if hasattr(student, key):
            setattr(student, key, value)
    db.session.commit()
    return {"success": True, "message": "Student updated successfully", "data": {"id": student.id}}, 200


@students_bp.route("/students/<int:student_id>", methods=["DELETE"])
@jwt_required()
@role_required("super_admin", "admin")
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    student.is_active = False
    student.status = "inactive"
    db.session.commit()
    return {"success": True, "message": "Student deactivated successfully"}, 200
