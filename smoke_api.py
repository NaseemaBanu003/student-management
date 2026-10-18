import os

os.environ.setdefault("FLASK_ENV", "testing")
os.environ.setdefault("TESTING", "1")
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import create_app
from app.extensions import db
from app.models import Role, User

app = create_app()
app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")

with app.app_context():
    db.create_all()
    role = Role(name="super_admin", description="Super admin")
    db.session.add(role)
    db.session.flush()
    user = User(username="superadmin", email="superadmin@example.com", first_name="Super", last_name="Admin", password="Admin@12345", is_active=True)
    user.roles.append(role)
    db.session.add(user)
    db.session.commit()

    client = app.test_client()
    login = client.post('/api/auth/login', json={'email': 'superadmin@example.com', 'password': 'Admin@12345'})
    token = login.get_json()['data']['access_token']
    me = client.get('/api/auth/me', headers={'Authorization': f'Bearer {token}'})
    dash = client.get('/api/dashboard/admin', headers={'Authorization': f'Bearer {token}'})

    with open(r'D:\smp\smoke_api_results.txt', 'w', encoding='utf-8') as fh:
        fh.write(f"LOGIN_STATUS={login.status_code}\n")
        fh.write(f"LOGIN_SUCCESS={login.get_json().get('success')}\n")
        fh.write(f"ME_STATUS={me.status_code}\n")
        fh.write(f"ME_SUCCESS={me.get_json().get('success')}\n")
        fh.write(f"DASH_STATUS={dash.status_code}\n")
        fh.write(f"DASH_SUCCESS={dash.get_json().get('success')}\n")
