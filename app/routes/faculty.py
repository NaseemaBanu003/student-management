from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Department, Faculty
from app.routes.auth import get_current_user, role_required

faculty_bp = Blueprint("faculty", __name__)


@faculty_bp.route("/faculty", methods=["GET"])
@jwt_required()
def list_faculty():
    faculty_members = Faculty.query.order_by(Faculty.id.desc()).all()
    payload = [{"id": f.id, "faculty_id": f.faculty_id, "full_name": f.full_name, "email": f.email, "designation": f.designation, "status": f.status} for f in faculty_members]
    return {"success": True, "data": payload}, 200


@faculty_bp.route("/faculty", methods=["POST"])
@jwt_required()
@role_required("super_admin", "admin")
def create_faculty():
    data = request.get_json(silent=True) or {}
    if not data.get("first_name") or not data.get("last_name") or not data.get("email"):
        return {"success": False, "message": "First name, last name, and email are required"}, 400
    department = db.session.get(Department, data.get("department_id"))
    if not department:
        return {"success": False, "message": "Invalid department"}, 400
    faculty = Faculty(
        faculty_id=f"FAC-{Faculty.query.count()+1:04d}",
        employee_id=f"EMP-{Faculty.query.count()+1:05d}",
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        phone=data.get("phone", ""),
        department_id=department.id,
        designation=data.get("designation", "Lecturer"),
        status=data.get("status", "active"),
    )
    db.session.add(faculty)
    db.session.commit()
    return {"success": True, "message": "Faculty created successfully", "data": {"id": faculty.id}}, 201


@faculty_bp.route("/faculty/<int:faculty_id>", methods=["GET"])
@jwt_required()
def get_faculty(faculty_id):
    faculty = Faculty.query.get_or_404(faculty_id)
    return {"success": True, "data": {"id": faculty.id, "full_name": faculty.full_name, "email": faculty.email, "department_id": faculty.department_id, "designation": faculty.designation}}, 200


@faculty_bp.route("/faculty/<int:faculty_id>", methods=["PUT"])
@jwt_required()
@role_required("super_admin", "admin")
def update_faculty(faculty_id):
    faculty = Faculty.query.get_or_404(faculty_id)
    data = request.get_json(silent=True) or {}
    for key, value in data.items():
        if hasattr(faculty, key):
            setattr(faculty, key, value)
    db.session.commit()
    return {"success": True, "message": "Faculty updated successfully"}, 200
