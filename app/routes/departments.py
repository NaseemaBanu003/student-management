from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Department
from app.routes.auth import role_required


departments_bp = Blueprint("departments", __name__)


@departments_bp.route("/departments", methods=["GET"])
@jwt_required()
def list_departments():
    departments = Department.query.order_by(Department.id.asc()).all()
    return {"success": True, "data": [{"id": d.id, "name": d.name, "code": d.code, "description": d.description, "is_active": d.is_active} for d in departments]}, 200


@departments_bp.route("/departments", methods=["POST"])
@jwt_required()
@role_required("super_admin", "admin")
def create_department():
    data = request.get_json(silent=True) or {}
    if not data.get("name") or not data.get("code"):
        return {"success": False, "message": "Name and code are required"}, 400
    department = Department(name=data["name"], code=data["code"], description=data.get("description", ""), head_name=data.get("head_name", ""))
    db.session.add(department)
    db.session.commit()
    return {"success": True, "message": "Department created successfully", "data": {"id": department.id}}, 201


@departments_bp.route("/departments/<int:department_id>", methods=["GET"])
@jwt_required()
def get_department(department_id):
    department = Department.query.get_or_404(department_id)
    return {"success": True, "data": {"id": department.id, "name": department.name, "code": department.code, "description": department.description, "is_active": department.is_active}}, 200


@departments_bp.route("/departments/<int:department_id>", methods=["PUT"])
@jwt_required()
@role_required("super_admin", "admin")
def update_department(department_id):
    department = Department.query.get_or_404(department_id)
    data = request.get_json(silent=True) or {}
    for key, value in data.items():
        if hasattr(department, key):
            setattr(department, key, value)
    db.session.commit()
    return {"success": True, "message": "Department updated successfully"}, 200
