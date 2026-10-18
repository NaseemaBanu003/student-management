from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Student, StudentFee, Payment
from app.routes.auth import role_required

fees_bp = Blueprint("fees", __name__)


@fees_bp.route("/fees", methods=["GET"])
@jwt_required()
def list_fees():
    records = StudentFee.query.order_by(StudentFee.id.desc()).limit(50).all()
    return {"success": True, "data": [{"id": r.id, "student_id": r.student_id, "total_amount": r.total_amount, "paid_amount": r.paid_amount, "status": r.status} for r in records]}, 200


@fees_bp.route("/fees", methods=["POST"])
@jwt_required()
@role_required("super_admin", "admin")
def create_fee():
    data = request.get_json(silent=True) or {}
    if not data.get("student_id"):
        return {"success": False, "message": "student_id is required"}, 400
    if not db.session.get(Student, data["student_id"]):
        return {"success": False, "message": "Student not found"}, 404
    fee = StudentFee(student_id=data["student_id"], category_id=data.get("category_id", 1), academic_year_id=data.get("academic_year_id", 1), total_amount=float(data.get("total_amount", 0)), paid_amount=float(data.get("paid_amount", 0)), status=data.get("status", "pending"))
    db.session.add(fee)
    db.session.commit()
    return {"success": True, "message": "Fee record created successfully", "data": {"id": fee.id}}, 201


@fees_bp.route("/payments", methods=["POST"])
@jwt_required()
@role_required("super_admin", "admin")
def record_payment():
    data = request.get_json(silent=True) or {}
    student_id = data.get("student_id")
    amount = float(data.get("amount", 0))
    if not student_id or amount <= 0:
        return {"success": False, "message": "Valid student_id and amount are required"}, 400
    payment = Payment(student_id=student_id, amount=amount, payment_method=data.get("payment_method", "manual"), payment_status="paid")
    db.session.add(payment)
    db.session.commit()
    return {"success": True, "message": "Payment recorded successfully", "data": {"id": payment.id}}, 201
