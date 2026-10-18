from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Attendance, Student, Subject, Faculty
from app.routes.auth import role_required

attendance_bp = Blueprint("attendance", __name__)


@attendance_bp.route("/attendance", methods=["GET"])
@jwt_required()
def list_attendance():
    records = Attendance.query.order_by(Attendance.attendance_date.desc()).limit(50).all()
    return {"success": True, "data": [{"id": r.id, "student_id": r.student_id, "subject_id": r.subject_id, "attendance_date": str(r.attendance_date), "status": r.status} for r in records]}, 200


@attendance_bp.route("/attendance", methods=["POST"])
@jwt_required()
@role_required("super_admin", "admin", "faculty")
def create_attendance():
    data = request.get_json(silent=True) or {}
    if not data.get("student_id") or not data.get("subject_id") or not data.get("faculty_id"):
        return {"success": False, "message": "student_id, subject_id, and faculty_id are required"}, 400
    if not db.session.get(Student, data["student_id"]) or not db.session.get(Subject, data["subject_id"]) or not db.session.get(Faculty, data["faculty_id"]):
        return {"success": False, "message": "Invalid references"}, 400
    attendance = Attendance(
        student_id=data["student_id"],
        subject_id=data["subject_id"],
        faculty_id=data["faculty_id"],
        attendance_date=data.get("attendance_date", str(date.today())),
        period=data.get("period", "1"),
        status=data.get("status", "present"),
        remarks=data.get("remarks", ""),
    )
    db.session.add(attendance)
    db.session.commit()
    return {"success": True, "message": "Attendance recorded successfully", "data": {"id": attendance.id}}, 201
