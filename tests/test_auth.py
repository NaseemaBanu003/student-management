import json


def test_login_success(client):
    from app.models import Role, User
    from app.extensions import db

    role = Role(name="super_admin", description="Super admin")
    db.session.add(role)
    db.session.flush()
    user = User(username="superadmin", email="superadmin@example.com", first_name="Super", last_name="Admin", password="Admin@12345", is_active=True)
    user.roles.append(role)
    db.session.add(user)
    db.session.commit()

    response = client.post('/api/auth/login', json={'email': 'superadmin@example.com', 'password': 'Admin@12345'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'access_token' in data['data']


def test_student_list_requires_auth(client):
    response = client.get('/api/students')
    assert response.status_code == 401


def test_create_department(client):
    from app.models import Role, User
    from app.extensions import db

    role = Role(name="admin", description="Admin")
    db.session.add(role)
    db.session.flush()
    user = User(username="adminuser", email="admin@example.com", first_name="Admin", last_name="User", password="Admin@12345", is_active=True)
    user.roles.append(role)
    db.session.add(user)
    db.session.commit()

    login = client.post('/api/auth/login', json={'email': 'admin@example.com', 'password': 'Admin@12345'})
    token = login.get_json()['data']['access_token']

    response = client.post('/api/departments', json={'name': 'Computer Science', 'code': 'CSE'}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['success'] is True
