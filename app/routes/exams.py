from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Exam, Course, Semester, Subject
from app.routes.auth import role_required

exams_bp = Blueprint("exams", __name__)


@exams_bp.route("/exams", methods=["GET"])
@jwt_required()
def list_exams():
    exams = Exam.query.order_by(Exam.exam_date.desc()).all()
    return {"success": True, "data": [{"id": e.id, "exam_name": e.exam_name, "exam_type": e.exam_type, "room": e.room, "exam_date": str(e.exam_date)} for e in exams]}, 200


@exams_bp.route("/exams", methods=["POST"])
@jwt_required()
@role_required("super_admin", "admin", "faculty")
def create_exam():
    data = request.get_json(silent=True) or {}
    if not data.get("exam_name") or not data.get("subject_id"):
        return {"success": False, "message": "Exam name and subject are required"}, 400
    if not db.session.get(Subject, data["subject_id"]):
        return {"success": False, "message": "Subject not found"}, 404
    exam = Exam(
        exam_name=data["exam_name"],
        exam_type=data.get("exam_type", "Internal"),
        subject_id=data["subject_id"],
        course_id=data.get("course_id", 1),
        semester_id=data.get("semester_id", 1),
        room=data.get("room", "A101"),
        exam_date=data.get("exam_date", "2026-01-01"),
        start_time=data.get("start_time", "09:00:00"),
        end_time=data.get("end_time", "11:00:00"),
    )
    db.session.add(exam)
    db.session.commit()
    return {"success": True, "message": "Exam created successfully", "data": {"id": exam.id}}, 201
