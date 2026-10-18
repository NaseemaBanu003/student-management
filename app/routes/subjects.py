from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Course, Department, Subject, Semester
from app.routes.auth import role_required

subjects_bp = Blueprint("subjects", __name__)


@subjects_bp.route("/subjects", methods=["GET"])
@jwt_required()
def list_subjects():
    subjects = Subject.query.order_by(Subject.id.asc()).all()
    return {"success": True, "data": [{"id": s.id, "code": s.code, "name": s.name, "credits": s.credits, "subject_type": s.subject_type} for s in subjects]}, 200


@subjects_bp.route("/subjects", methods=["POST"])
@jwt_required()
@role_required("super_admin", "admin")
def create_subject():
    data = request.get_json(silent=True) or {}
    if not data.get("code") or not data.get("name") or not data.get("department_id") or not data.get("course_id") or not data.get("semester_id"):
        return {"success": False, "message": "Subject code, name, department, course and semester are required"}, 400
    if not db.session.get(Department, data["department_id"]):
        return {"success": False, "message": "Department not found"}, 404
    if not db.session.get(Course, data["course_id"]):
        return {"success": False, "message": "Course not found"}, 404
    if not db.session.get(Semester, data["semester_id"]):
        return {"success": False, "message": "Semester not found"}, 404
    subject = Subject(code=data["code"], name=data["name"], description=data.get("description", ""), credits=int(data.get("credits", 4)), department_id=data["department_id"], course_id=data["course_id"], semester_id=data["semester_id"], subject_type=data.get("subject_type", "Theory"))
    db.session.add(subject)
    db.session.commit()
    return {"success": True, "message": "Subject created successfully", "data": {"id": subject.id}}, 201
