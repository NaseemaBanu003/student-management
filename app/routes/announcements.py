from datetime import datetime, timezone

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Announcement
from app.routes.auth import role_required

announcements_bp = Blueprint("announcements", __name__)


@announcements_bp.route("/announcements", methods=["GET"])
@jwt_required()
def list_announcements():
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    payload = [{"id": a.id, "title": a.title, "audience": a.audience, "is_published": a.is_published, "created_at": str(a.created_at)} for a in announcements]
    return {"success": True, "data": payload}, 200


@announcements_bp.route("/announcements", methods=["POST"])
@jwt_required()
@role_required("super_admin", "admin", "faculty")
def create_announcement():
    data = request.get_json(silent=True) or {}
    if not data.get("title") or not data.get("content"):
        return {"success": False, "message": "Title and content are required"}, 400
    announcement = Announcement(
        title=data["title"],
        content=data["content"],
        audience=data.get("audience", "everyone"),
        is_published=data.get("is_published", True),
        published_at=datetime.now(timezone.utc) if data.get("is_published") else None,
        created_by=data.get("created_by", 1),
    )
    db.session.add(announcement)
    db.session.commit()
    return {"success": True, "message": "Announcement created successfully", "data": {"id": announcement.id}}, 201
