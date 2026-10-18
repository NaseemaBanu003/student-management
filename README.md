# EduManage Pro

EduManage Pro is a production-style student management platform built with Flask, PostgreSQL, SQLAlchemy, JWT authentication, and a modern HTML/CSS/JS frontend.

## Features

- Role-based access control for Super Admin, Admin, Faculty, and Student roles
- Student, faculty, department, course, subject, attendance, exam, marks, fee, announcement, report, and document management
- JWT authentication with refresh token flow
- PostgreSQL-ready relational model with SQLAlchemy
- Flask-Migrate/Alembic migration support
- Frontend dashboard and login flow using static HTML/CSS/JS
- Pytest-based API testing and validation coverage
- Dockerized deployment-ready setup

## Demo credentials

- Super Admin: superadmin@edumanagepro.edu / Admin@12345
- Admin: admin@edumanagepro.edu / Admin@12345
- Faculty: faculty@edumanagepro.edu / Faculty@12345
- Student: student@edumanagepro.edu / Student@12345

## Local setup

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   . .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Copy environment variables:
   ```bash
   cp .env.example .env
   ```
3. Start PostgreSQL and run migrations:
   ```bash
   flask db init
   flask db migrate -m "initial migration"
   flask db upgrade
   ```
4. Seed demo data:
   ```bash
   python scripts/seed_demo.py
   ```
5. Start the app:
   ```bash
   python run.py
   ```

## API overview

- POST /api/auth/login
- POST /api/auth/refresh
- POST /api/auth/logout
- GET /api/dashboard/admin
- GET /api/students
- POST /api/students
- GET /api/faculty
- GET /api/departments
- GET /api/courses
- GET /api/subjects
- GET /api/attendance
- GET /api/exams
- GET /api/marks
- GET /api/fees
- GET /api/announcements
- GET /api/reports/attendance
- GET /api/reports/performance

## Testing

```bash
pytest
```

## Production notes

- Use environment variables for all secrets and database credentials.
- Keep PostgreSQL as the production database.
- File uploads are stored in the configured upload folder.
- CORS, rate limiting, JWT rotation, and validation are included at the application layer.
