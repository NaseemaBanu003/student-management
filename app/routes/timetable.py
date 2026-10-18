from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import TimetableEntry, Course, Semester, Subject, Faculty
from app.routes.auth import role_required


timetable_bp = Blueprint("timetable", __name__)


@timetable_bp.route("/timetable", methods=["GET"])
@jwt_required()
def list_timetable():
    entries = TimetableEntry.query.order_by(TimetableEntry.day.asc()).all()
    return {"success": True, "data": [{"id": e.id, "day": e.day, "subject_id": e.subject_id, "faculty_id": e.faculty_id, "room": e.room} for e in entries]}, 200


@timetable_bp.route("/timetable", methods=["POST"])
@jwt_required()
@role_required("super_admin", "admin")
def create_timetable():
    data = request.get_json(silent=True) or {}
    if not data.get("day") or not data.get("subject_id") or not data.get("faculty_id") or not data.get("room"):
        return {"success": False, "message": "Day, subject, faculty, and room are required"}, 400
    if not db.session.get(Subject, data["subject_id"]) or not db.session.get(Faculty, data["faculty_id"]):
        return {"success": False, "message": "Invalid subject or faculty"}, 400
    entry = TimetableEntry(
        day=data["day"],
        start_time=data.get("start_time", "09:00:00"),
        end_time=data.get("end_time", "10:00:00"),
        room=data["room"],
        section=data.get("section", "A"),
        academic_year_id=data.get("academic_year_id", 1),
        course_id=data.get("course_id", 1),
        semester_id=data.get("semester_id", 1),
        subject_id=data["subject_id"],
        faculty_id=data["faculty_id"],
    )
    db.session.add(entry)
    db.session.commit()
    return {"success": True, "message": "Timetable entry created successfully", "data": {"id": entry.id}}, 201
