from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Mark, Student, Subject, Exam
from app.routes.auth import role_required

marks_bp = Blueprint("marks", __name__)


@marks_bp.route("/marks", methods=["GET"])
@jwt_required()
def list_marks():
    marks = Mark.query.order_by(Mark.id.desc()).limit(50).all()
    return {"success": True, "data": [{"id": m.id, "student_id": m.student_id, "subject_id": m.subject_id, "marks_obtained": m.marks_obtained, "grade": m.grade} for m in marks]}, 200


@marks_bp.route("/marks", methods=["POST"])
@jwt_required()
@role_required("super_admin", "admin", "faculty")
def create_mark():
    data = request.get_json(silent=True) or {}
    if not data.get("student_id") or not data.get("subject_id") or not data.get("exam_id"):
        return {"success": False, "message": "student_id, subject_id, and exam_id are required"}, 400
    if not db.session.get(Student, data["student_id"]) or not db.session.get(Subject, data["subject_id"]) or not db.session.get(Exam, data["exam_id"]):
        return {"success": False, "message": "Invalid mark references"}, 400
    marks = float(data.get("marks_obtained", 0))
    percent = (marks / max(float(data.get("maximum_marks", 100.0)), 1)) * 100
    grade = "A+" if percent >= 90 else "A" if percent >= 80 else "B+" if percent >= 70 else "B" if percent >= 60 else "C" if percent >= 50 else "D" if percent >= 40 else "F"
    point = 4.0 if grade == "A+" else 3.7 if grade == "A" else 3.3 if grade == "B+" else 3.0 if grade == "B" else 2.0 if grade == "C" else 1.0 if grade == "D" else 0.0
    mark = Mark(student_id=data["student_id"], subject_id=data["subject_id"], exam_id=data["exam_id"], maximum_marks=float(data.get("maximum_marks", 100.0)), marks_obtained=marks, grade=grade, grade_point=point, remarks=data.get("remarks", ""))
    db.session.add(mark)
    db.session.commit()
    return {"success": True, "message": "Mark recorded successfully", "data": {"id": mark.id, "grade": mark.grade}}, 201
