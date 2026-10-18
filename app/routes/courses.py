from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Course, Department
from app.routes.auth import role_required

courses_bp = Blueprint("courses", __name__)


@courses_bp.route("/courses", methods=["GET"])
@jwt_required()
def list_courses():
    courses = Course.query.order_by(Course.id.asc()).all()
    return {"success": True, "data": [{"id": c.id, "code": c.code, "name": c.name, "degree_type": c.degree_type, "status": c.status} for c in courses]}, 200


@courses_bp.route("/courses", methods=["POST"])
@jwt_required()
@role_required("super_admin", "admin")
def create_course():
    data = request.get_json(silent=True) or {}
    if not data.get("name") or not data.get("code") or not data.get("department_id"):
        return {"success": False, "message": "Course name, code, and department are required"}, 400
    if db.session.get(Department, data["department_id"]) is None:
        return {"success": False, "message": "Department not found"}, 404
    course = Course(code=data["code"], name=data["name"], degree_type=data.get("degree_type", "B.Tech"), duration=int(data.get("duration", 4)), total_semesters=int(data.get("total_semesters", 8)), description=data.get("description", ""), department_id=data["department_id"], status=data.get("status", "active"))
    db.session.add(course)
    db.session.commit()
    return {"success": True, "message": "Course created successfully", "data": {"id": course.id}}, 201
