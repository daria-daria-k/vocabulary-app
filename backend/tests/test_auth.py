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

def test_login_rate_limit(client, registered_user):
    """После 5 неудачных попыток вход блокируется (429)"""
    wrong = {"email": registered_user["email"], "password": "неверный"}

    for _ in range(5):
        response = client.post("/auth/login", json=wrong)
        assert response.status_code == 401

    response = client.post("/auth/login", json=wrong)
    assert response.status_code == 429


def test_login_reset_rate_limit(client, registered_user):
    """Сброс кеша redis при одной из удачных попыток входа"""
    wrong = {"email": registered_user["email"], "password": ""}
    success = {"email": registered_user["email"], "password": registered_user["password"]}

    for _ in range(4):
        response = client.post("/auth/login", json=wrong)
        assert response.status_code == 401

    response = client.post("/auth/login", json=success)
    assert response.status_code == 200

    for _ in range(3):
        response = client.post("/auth/login", json=wrong)
        assert response.status_code == 401

def test_register_weak_password(client):
    """Слабый пароль (короткий, без цифры) отклоняется с 422"""
    response = client.post(
        "/auth/register",
        json={"email": "test@mail.ru", "password": "123fg"}
    )

    assert response.status_code == 422


def test_register_only_words_password(client):
    """Слабый пароль (только буквы) отклоняется с 422"""
    response = client.post(
        "/auth/register",
        json={"email": "test@mail.ru", "password": "jfhytghnbc"}
    )

    assert response.status_code == 422


def test_register_only_numbers_password(client):
    """Слабый пароль (только цифры) отклоняется с 422"""
    response = client.post(
        "/auth/register",
        json={"email": "test@mail.ru", "password": "123456789"}
    )

    assert response.status_code == 422


def test_register_valid_password(client):
    """Слабый пароль (только цифры) отклоняется с 422"""
    response = client.post(
        "/auth/register",
        json={"email": "test@mail.ru", "password": "test1234ik"}
    )

    assert response.status_code == 200


def test_register_invalid_email(client):
    """Некорректный email отклоняется с 422"""
    response = client.post(
        "/auth/register",
        json={"email": "email", "password": "test123kihyb"}
    )
    assert response.status_code == 422
