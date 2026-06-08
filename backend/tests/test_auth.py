def test_register(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "test@mail.ru",
            "password": "test123",
        }
    )
    email = response.json()["email"]

    assert response.status_code == 200
    assert email == "test@mail.ru"

def test_register_duplicate(client):
    client.post(
        "/auth/register",
        json={
            "email": "test@mail.ru",
            "password": "test123",
        }
    )

    response = client.post(
        "/auth/register",
        json={
            "email": "test@mail.ru",
            "password": "test123",
        }
    )

    assert response.status_code == 400

def test_login(client):
    client.post(
        "/auth/register",
        json={
            "email": "test@mail.ru",
            "password": "test123",
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "test@mail.ru",
            "password": "test123",
        }
    )

    assert response.status_code == 200
    assert response.json()["access_token"] is not None

def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={
            "email": "test@mail.ru",
            "password": "test123",
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "test@mail.ru",
            "password": "1111",
        }
    )

    assert response.status_code == 401

def test_me_without_token(client):
    response = client.get(
        "/auth/me"
    )

    assert response.status_code == 401