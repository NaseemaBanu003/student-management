from datetime import datetime, timezone

from app.models import Announcement, Attendance, Department, Faculty, Student, StudentFee


def build_dashboard_summary():
    return {
        "total_students": Student.query.count(),
        "active_students": Student.query.filter_by(is_active=True).count(),
        "total_faculty": Faculty.query.count(),
        "departments": Department.query.count(),
        "subjects": 0,
        "students_by_department": [],
        "attendance_summary": [],
        "fee_summary": {"pending": StudentFee.query.filter_by(status="pending").count(), "paid": StudentFee.query.filter_by(status="paid").count()},
        "recent_announcements": [
            {"title": item.title, "created_at": item.created_at.isoformat()} for item in Announcement.query.order_by(Announcement.created_at.desc()).limit(5).all()
        ],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
