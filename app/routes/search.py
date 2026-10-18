from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.models import Course, Department, Faculty, Student, Subject
from app.routes.auth import role_required

search_bp = Blueprint("search", __name__)


@search_bp.route("/search", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin", "faculty", "student")
def global_search():
    query = request.args.get("q", "")
    if not query:
        return {"success": True, "data": {"students": [], "faculty": [], "courses": [], "departments": [], "subjects": []}}, 200
    results = {
        "students": [{"id": s.id, "name": s.full_name, "email": s.email} for s in Student.query.filter(Student.first_name.ilike(f"%{query}%")).limit(10).all()],
        "faculty": [{"id": f.id, "name": f.full_name, "email": f.email} for f in Faculty.query.filter(Faculty.first_name.ilike(f"%{query}%")).limit(10).all()],
        "courses": [{"id": c.id, "name": c.name} for c in Course.query.filter(Course.name.ilike(f"%{query}%")).limit(10).all()],
        "departments": [{"id": d.id, "name": d.name} for d in Department.query.filter(Department.name.ilike(f"%{query}%")).limit(10).all()],
        "subjects": [{"id": s.id, "name": s.name} for s in Subject.query.filter(Subject.name.ilike(f"%{query}%")).limit(10).all()],
    }
    return {"success": True, "data": results}, 200
