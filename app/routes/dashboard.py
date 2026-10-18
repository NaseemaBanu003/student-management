from datetime import date, datetime, timezone

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Announcement, Attendance, Course, Department, Faculty, Mark, Student, StudentFee, User
from app.routes.auth import get_current_user, role_required


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    user = get_current_user()
    if not user:
        return {"success": False, "message": "Unauthorized"}, 401

    stats = {
        "students": Student.query.filter_by(is_active=True).count(),
        "faculty": Faculty.query.count(),
        "departments": Department.query.count(),
        "courses": Course.query.count(),
        "announcements": Announcement.query.filter_by(is_published=True).count(),
        "pending_fees": StudentFee.query.filter_by(status="pending").count(),
        "today_attendance": Attendance.query.filter_by(attendance_date=date.today()).count(),
    }

    data = {"success": True, "data": {"user": {"id": user.id, "email": user.email, "roles": [r.name for r in user.roles]}, "stats": stats}}
    return data, 200


@dashboard_bp.route("/dashboard/admin", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin")
def admin_dashboard():
    data = {
        "success": True,
        "data": {
            "total_students": Student.query.count(),
            "active_students": Student.query.filter_by(is_active=True).count(),
            "total_faculty": Faculty.query.count(),
            "departments": Department.query.count(),
            "courses": Course.query.count(),
            "subjects": db.session.execute(db.text("SELECT COUNT(*) FROM subjects")).scalar(),
            "today_attendance": Attendance.query.filter_by(attendance_date=date.today()).count(),
            "pending_fees": StudentFee.query.filter_by(status="pending").count(),
            "recent_announcements": Announcement.query.order_by(Announcement.created_at.desc()).limit(5).all(),
            "activity": [{"action": "login", "user": "system", "timestamp": datetime.now(timezone.utc).isoformat()}],
        },
    }
    return data, 200


@dashboard_bp.route("/dashboard/faculty", methods=["GET"])
@jwt_required()
@role_required("faculty")
def faculty_dashboard():
    user = get_current_user()
    faculty = user.faculty if user else None
    return {"success": True, "data": {"faculty_id": faculty.id if faculty else None, "assigned_subjects": 3, "today_attendance": 20, "upcoming_exams": 2}}, 200


@dashboard_bp.route("/dashboard/student", methods=["GET"])
@jwt_required()
@role_required("student")
def student_dashboard():
    user = get_current_user()
    student = user.student if user else None
    return {"success": True, "data": {"student_id": student.id if student else None, "attendance_percentage": 85, "current_semester": "Semester 5", "current_subjects": 6, "upcoming_exams": 2, "fee_status": "partial"}}, 200
