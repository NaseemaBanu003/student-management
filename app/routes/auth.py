from datetime import datetime, timezone
from functools import wraps

from flask import Blueprint, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
    unset_jwt_cookies,
)
from webargs import fields
from webargs.flaskparser import use_args

from app.extensions import db, limiter
from app.models import User
from app.schemas import ChangePasswordSchema, LoginSchema


auth_bp = Blueprint("auth", __name__)


def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = db.session.get(User, user_id) if user_id is not None else None
            if not user or not user.is_active:
                return {"success": False, "message": "Account is disabled or invalid"}, 401
            if roles and not any(user.has_role(role) for role in roles):
                return {"success": False, "message": "Forbidden: insufficient permissions"}, 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def get_current_user():
    user_id = get_jwt_identity()
    if not user_id:
        return None
    return db.session.get(User, user_id)


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("10/minute")
def login():
    payload = request.get_json(silent=True) or {}
    errors = LoginSchema().validate(payload)
    if errors:
        return {"success": False, "message": "Validation failed", "errors": errors}, 400

    user = User.query.filter_by(email=payload["email"]).first()
    if not user or not user.verify_password(payload["password"]):
        return {"success": False, "message": "Invalid email or password"}, 401

    if not user.is_active:
        return {"success": False, "message": "Account is inactive"}, 401

    access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.roles[0].name if user.roles else "student"})
    refresh_token = create_refresh_token(identity=str(user.id))

    user.last_login = datetime.now(timezone.utc)
    db.session.commit()

    return {
        "success": True,
        "message": "Login successful",
        "data": {
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "roles": [role.name for role in user.roles],
            },
            "access_token": access_token,
            "refresh_token": refresh_token,
        },
    }, 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    if not user or not user.is_active:
        return {"success": False, "message": "User not found or inactive"}, 401
    access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.roles[0].name if user.roles else "student"})
    return {"success": True, "data": {"access_token": access_token}}, 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    response = {"success": True, "message": "Logged out successfully"}
    unset_jwt_cookies(response)
    return response, 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user = get_current_user()
    if not user:
        return {"success": False, "message": "Unauthorized"}, 401
    return {"success": True, "data": {"user": {"id": user.id, "email": user.email, "username": user.username, "first_name": user.first_name, "last_name": user.last_name, "roles": [r.name for r in user.roles]}}}, 200


@auth_bp.route("/change-password", methods=["POST"])
@jwt_required()
def change_password():
    payload = request.get_json(silent=True) or {}
    errors = ChangePasswordSchema().validate(payload)
    if errors:
        return {"success": False, "message": "Validation failed", "errors": errors}, 400

    user = get_current_user()
    if not user.verify_password(payload["current_password"]):
        return {"success": False, "message": "Current password is incorrect"}, 400

    user.password = payload["new_password"]
    db.session.commit()
    return {"success": True, "message": "Password changed successfully"}, 200


@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    payload = request.get_json(silent=True) or {}
    email = payload.get("email")
    if not email:
        return {"success": False, "message": "Email is required"}, 400
    user = User.query.filter_by(email=email).first()
    if user:
        return {"success": True, "message": "If an account exists, a password reset link has been sent"}, 200
    return {"success": True, "message": "If an account exists, a password reset link has been sent"}, 200


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    payload = request.get_json(silent=True) or {}
    token = payload.get("token")
    password = payload.get("password")
    if not token or not password:
        return {"success": False, "message": "Token and password are required"}, 400
    return {"success": True, "message": "Password reset was simulated successfully"}, 200


@auth_bp.route("/deactivate", methods=["POST"])
@jwt_required()
def deactivate_account():
    user = get_current_user()
    if not user:
        return {"success": False, "message": "Unauthorized"}, 401
    user.is_active = False
    db.session.commit()
    return {"success": True, "message": "Account deactivated"}, 200
