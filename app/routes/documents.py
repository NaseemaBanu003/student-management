import os
from werkzeug.utils import secure_filename
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Document
from app.routes.auth import role_required, get_current_user


documents_bp = Blueprint("documents", __name__)


@documents_bp.route("/documents", methods=["GET"])
@jwt_required()
def list_documents():
    docs = Document.query.order_by(Document.created_at.desc()).all()
    return {"success": True, "data": [{"id": d.id, "title": d.title, "filename": d.filename, "document_type": d.document_type} for d in docs]}, 200


@documents_bp.route("/documents/upload", methods=["POST"])
@jwt_required()
@role_required("super_admin", "admin", "faculty")
def upload_document():
    user = get_current_user()
    if not user:
        return {"success": False, "message": "Unauthorized"}, 401
    if "file" not in request.files:
        return {"success": False, "message": "No file part"}, 400
    file = request.files["file"]
    if file.filename == "":
        return {"success": False, "message": "No selected file"}, 400
    filename = secure_filename(file.filename)
    allowed_types = {"pdf", "doc", "docx", "txt", "png", "jpg", "jpeg"}
    if "." not in filename or filename.rsplit(".", 1)[1].lower() not in allowed_types:
        return {"success": False, "message": "Unsupported file type"}, 400
    upload_dir = os.getenv("UPLOAD_FOLDER", "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    storage_path = os.path.join(upload_dir, filename)
    file.save(storage_path)
    doc = Document(title=request.form.get("title", filename), filename=filename, content_type=file.mimetype or "application/octet-stream", file_size=os.path.getsize(storage_path), storage_path=storage_path, document_type=request.form.get("document_type", "general"), uploaded_by=user.id)
    db.session.add(doc)
    db.session.commit()
    return {"success": True, "message": "Document uploaded successfully", "data": {"id": doc.id}}, 201
