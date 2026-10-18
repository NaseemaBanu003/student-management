from app.routes.announcements import announcements_bp
from app.routes.attendance import attendance_bp
from app.routes.auth import auth_bp
from app.routes.dashboard import dashboard_bp
from app.routes.departments import departments_bp
from app.routes.documents import documents_bp
from app.routes.exams import exams_bp
from app.routes.faculty import faculty_bp
from app.routes.fees import fees_bp
from app.routes.marks import marks_bp
from app.routes.notifications import notifications_bp
from app.routes.reports import reports_bp
from app.routes.search import search_bp
from app.routes.students import students_bp
from app.routes.subjects import subjects_bp
from app.routes.courses import courses_bp
from app.routes.timetable import timetable_bp
from app.routes.web import web_bp


def register_blueprints(app):
    app.register_blueprint(web_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/api")
    app.register_blueprint(students_bp, url_prefix="/api")
    app.register_blueprint(faculty_bp, url_prefix="/api")
    app.register_blueprint(departments_bp, url_prefix="/api")
    app.register_blueprint(courses_bp, url_prefix="/api")
    app.register_blueprint(subjects_bp, url_prefix="/api")
    app.register_blueprint(attendance_bp, url_prefix="/api")
    app.register_blueprint(exams_bp, url_prefix="/api")
    app.register_blueprint(marks_bp, url_prefix="/api")
    app.register_blueprint(fees_bp, url_prefix="/api")
    app.register_blueprint(announcements_bp, url_prefix="/api")
    app.register_blueprint(reports_bp, url_prefix="/api")
    app.register_blueprint(search_bp, url_prefix="/api")
    app.register_blueprint(notifications_bp, url_prefix="/api")
    app.register_blueprint(documents_bp, url_prefix="/api")
    app.register_blueprint(timetable_bp, url_prefix="/api")
