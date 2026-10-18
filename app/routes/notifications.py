from flask import Blueprint
from flask_jwt_extended import jwt_required

from app.models import Notification
from app.routes.auth import get_current_user, role_required

notifications_bp = Blueprint("notifications", __name__)


@notifications_bp.route("/notifications", methods=["GET"])
@jwt_required()
def list_notifications():
    user = get_current_user()
    if not user:
        return {"success": False, "message": "Unauthorized"}, 401
    notifications = Notification.query.filter_by(user_id=user.id).order_by(Notification.created_at.desc()).all()
    return {"success": True, "data": [{"id": n.id, "title": n.title, "message": n.message, "is_read": n.is_read} for n in notifications]}, 200
