from app import create_app
from app.extensions import db
from app.models import AcademicYear, Announcement, Attendance, Course, Department, Faculty, FeeCategory, Role, Semester, Student, Subject, User
from app.models.user import Permission


def seed_database():
    app = create_app()
    with app.app_context():
        db.create_all()

        if not Role.query.filter_by(name="super_admin").first():
            super_admin_role = Role(name="super_admin", description="Super administrator")
            admin_role = Role(name="admin", description="Institution administrator")
            faculty_role = Role(name="faculty", description="Faculty member")
            student_role = Role(name="student", description="Student user")
            db.session.add_all([super_admin_role, admin_role, faculty_role, student_role])

        if not Permission.query.filter_by(name="manage_students").first():
            permissions = [
                Permission(name="manage_students", description="Manage student records"),
                Permission(name="manage_faculty", description="Manage faculty records"),
                Permission(name="manage_courses", description="Manage course records"),
                Permission(name="manage_departments", description="Manage department records"),
                Permission(name="view_reports", description="View reports"),
            ]
            db.session.add_all(permissions)
            db.session.commit()

        dept = Department.query.filter_by(code="CSE").first()
        if not dept:
            dept = Department(name="Computer Science", code="CSE", description="Core computing programs", head_name="Dr. Anita Rao")
            db.session.add(dept)
            db.session.flush()

        course = Course.query.filter_by(code="BTECH-CSE").first()
        if not course:
            course = Course(code="BTECH-CSE", name="B.Tech Computer Science", degree_type="B.Tech", duration=4, total_semesters=8, description="Engineering program", department_id=dept.id, status="active")
            db.session.add(course)
            db.session.flush()

        academic_year = AcademicYear.query.filter_by(name="2026-27").first()
        if not academic_year:
            academic_year = AcademicYear(name="2026-27", start_date="2026-07-01", end_date="2027-06-30", is_active=True)
            db.session.add(academic_year)
            db.session.flush()

        semester = Semester.query.filter_by(name="Semester 1").first()
        if not semester:
            semester = Semester(name="Semester 1", order=1, is_active=True)
            db.session.add(semester)
            db.session.flush()

        subject = Subject.query.filter_by(code="CS101").first()
        if not subject:
            subject = Subject(code="CS101", name="Programming Fundamentals", description="Intro to programming", credits=4, department_id=dept.id, course_id=course.id, semester_id=semester.id, subject_type="Theory")
            db.session.add(subject)
            db.session.flush()

        super_user = User.query.filter_by(email="superadmin@edumanagepro.edu").first()
        if not super_user:
            super_user = User(username="superadmin", email="superadmin@edumanagepro.edu", first_name="System", last_name="Admin", password="Admin@12345", is_active=True)
            db.session.add(super_user)
            db.session.flush()
            super_user.roles.append(Role.query.filter_by(name="super_admin").first())

        admin_user = User.query.filter_by(email="admin@edumanagepro.edu").first()
        if not admin_user:
            admin_user = User(username="admin", email="admin@edumanagepro.edu", first_name="College", last_name="Admin", password="Admin@12345", is_active=True)
            db.session.add(admin_user)
            db.session.flush()
            admin_user.roles.append(Role.query.filter_by(name="admin").first())

        faculty_user = User.query.filter_by(email="faculty@edumanagepro.edu").first()
        if not faculty_user:
            faculty_user = User(username="faculty", email="faculty@edumanagepro.edu", first_name="Nisha", last_name="Sharma", password="Faculty@12345", is_active=True)
            db.session.add(faculty_user)
            db.session.flush()
            faculty_user.roles.append(Role.query.filter_by(name="faculty").first())

        student_user = User.query.filter_by(email="student@edumanagepro.edu").first()
        if not student_user:
            student_user = User(username="student", email="student@edumanagepro.edu", first_name="Arjun", last_name="Mehta", password="Student@12345", is_active=True)
            db.session.add(student_user)
            db.session.flush()
            student_user.roles.append(Role.query.filter_by(name="student").first())

        if not Faculty.query.filter_by(email="faculty@edumanagepro.edu").first():
            faculty = Faculty(faculty_id="FAC-1001", employee_id="EMP-1001", first_name="Nisha", last_name="Sharma", email="faculty@edumanagepro.edu", phone="9876543210", department_id=dept.id, designation="Professor", status="active", user_id=faculty_user.id)
            db.session.add(faculty)
            db.session.flush()

        if not Student.query.filter_by(email="student@edumanagepro.edu").first():
            student = Student(student_id="STU-1001", admission_number="ADM-1001", first_name="Arjun", last_name="Mehta", email="student@edumanagepro.edu", phone="9988776655", department_id=dept.id, course_id=course.id, batch="2026", academic_year_id=academic_year.id, semester_id=semester.id, section="A", admission_date="2026-07-01", status="active", is_active=True, user_id=student_user.id)
            db.session.add(student)
            db.session.flush()

        if not FeeCategory.query.filter_by(name="Tuition").first():
            tuition = FeeCategory(name="Tuition", description="Tuition fee")
            hostel = FeeCategory(name="Hostel", description="Hostel fee")
            exam = FeeCategory(name="Examination", description="Exam fee")
            db.session.add_all([tuition, hostel, exam])

        if not Announcement.query.filter_by(title="Welcome to the new academic year").first():
            db.session.add(Announcement(title="Welcome to the new academic year", content="Welcome to EduManage Pro. All classes begin promptly on Monday.", audience="everyone", is_published=True, created_by=super_user.id))

        db.session.commit()
        print("Demo data seeded successfully.")


if __name__ == "__main__":
    seed_database()
