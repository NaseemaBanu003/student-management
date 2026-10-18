from marshmallow import Schema, fields, validate


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))


class ChangePasswordSchema(Schema):
    current_password = fields.String(required=True)
    new_password = fields.String(required=True, validate=validate.Length(min=8))


class PaginationSchema(Schema):
    page = fields.Integer(load_default=1, validate=validate.Range(min=1))
    per_page = fields.Integer(load_default=20, validate=validate.Range(min=1, max=100))
    search = fields.String(load_default="")


class StudentSchema(Schema):
    first_name = fields.String(required=True, validate=validate.Length(min=1, max=80))
    last_name = fields.String(required=True, validate=validate.Length(min=1, max=80))
    email = fields.Email(required=True)
    phone = fields.String(required=True)
    department_id = fields.Integer(required=True)
    course_id = fields.Integer(required=True)
    academic_year_id = fields.Integer(required=True)
    semester_id = fields.Integer(required=True)
    section = fields.String(load_default="A")


class FacultySchema(Schema):
    first_name = fields.String(required=True, validate=validate.Length(min=1, max=80))
    last_name = fields.String(required=True, validate=validate.Length(min=1, max=80))
    email = fields.Email(required=True)
    phone = fields.String(required=True)
    department_id = fields.Integer(required=True)
    designation = fields.String(load_default="Lecturer")


class DepartmentSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=2, max=120))
    code = fields.String(required=True, validate=validate.Length(min=2, max=20))
    description = fields.String(load_default="")
    head_name = fields.String(load_default="")


class SubjectSchema(Schema):
    code = fields.String(required=True)
    name = fields.String(required=True)
    credits = fields.Integer(required=True, validate=validate.Range(min=1, max=10))
    department_id = fields.Integer(required=True)
    course_id = fields.Integer(required=True)
    semester_id = fields.Integer(required=True)
    subject_type = fields.String(load_default="Theory")


__all__ = [
    "LoginSchema",
    "ChangePasswordSchema",
    "PaginationSchema",
    "StudentSchema",
    "FacultySchema",
    "DepartmentSchema",
    "SubjectSchema",
]
