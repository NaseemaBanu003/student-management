from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.models import Attendance, Mark, Student, StudentFee
from app.routes.auth import role_required

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/reports/attendance", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin")
def attendance_report():
    records = Attendance.query.order_by(Attendance.attendance_date.desc()).limit(20).all()
    payload = [{"id": r.id, "student_id": r.student_id, "subject_id": r.subject_id, "status": r.status, "attendance_date": str(r.attendance_date)} for r in records]
    return {"success": True, "data": payload}, 200


@reports_bp.route("/reports/performance", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin", "faculty")
def performance_report():
    marks = Mark.query.order_by(Mark.id.desc()).limit(20).all()
    payload = [{"id": m.id, "student_id": m.student_id, "subject_id": m.subject_id, "grade": m.grade, "marks_obtained": m.marks_obtained} for m in marks]
    return {"success": True, "data": payload}, 200


@reports_bp.route("/reports/fees", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin")
def fee_report():
    total_students = Student.query.count()
    total_fee = sum(f.total_amount for f in StudentFee.query.all())
    paid = sum(f.paid_amount for f in StudentFee.query.all())
    return {"success": True, "data": {"student_count": total_students, "total_fee": total_fee, "paid": paid, "pending": total_fee - paid}}, 200
