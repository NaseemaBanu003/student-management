import os

import pytest

os.environ.setdefault("FLASK_ENV", "testing")
os.environ.setdefault("TESTING", "1")
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import create_app
from app.extensions import db


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()


@pytest.fixture()
def client(app):
    return app.test_client()
