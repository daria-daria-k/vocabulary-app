def test_register(client, user_data):
    """Успешная регистрация пользователя"""
    response = client.post(
        "/auth/register",
        json=user_data
    )
    email = response.json()["email"]

    assert response.status_code == 200
    assert email == user_data["email"]


def test_register_duplicate(client, registered_user):
    """Повторная регистрация с тем же email возвращает 400"""
    response = client.post(
        "/auth/register",
        json=registered_user
    )

    assert response.status_code == 400


def test_login(client, registered_user):
    """Вход с верными данными возвращает токен"""
    response = client.post(
        "/auth/login",
        json=registered_user
    )

    assert response.status_code == 200
    assert response.json()["access_token"] is not None


def test_login_wrong_password(client, registered_user):
    """Вход с неверным паролем возвращает 401"""
    user_info = registered_user
    user_info["password"] = "1234"

    response = client.post(
        "/auth/login",
        json=user_info
    )

    assert response.status_code == 401


def test_me_without_token(client):
    """Запрос к /auth/me без токена возвращает 401"""
    response = client.get(
        "/auth/me"
    )

    assert response.status_code == 401


def test_me_with_token(client, auth_headers):
    """Запрос к /auth/me с валидным токеном возвращает данные пользователя"""
    response = client.get("/auth/me", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["email"] is not None