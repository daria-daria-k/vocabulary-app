def test_create_word(created_word):
    """Создание слова с валидным токеном, возвращает id слова"""
    response = created_word

    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert len(data["translations"]) == 1
    assert len(data["examples"]) == 1


def test_create_word_no_auth(client):
    """Создание слова без токена аутентификации"""
    response = client.post(
        "/words",
        json={
            "word_en": "apple",
            "translations": [{
                "translation_ru": "яблоко"
            }],
            "examples": [
                {
                    "sentence": "I ate an apple"
                }
            ]
        },
    )

    assert response.status_code == 401


def test_get_words_empty(client, auth_headers):
    """Пустой список слов у нового пользователя"""
    response = client.get(
        "/words",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == []


def test_get_not_found_word(client, auth_headers):
    """Поиск несуществующего слова"""
    response = client.get(
        "/words/999",
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_get_one_word(client, created_word, auth_headers):
    """Получение одного слова по id"""
    response = created_word

    data = response.json()
    word_id = data["id"]

    response_get_word = client.get(
        f"/words/{word_id}",
        headers=auth_headers,
    )

    assert response_get_word.status_code == 200
    new_word = response_get_word.json()
    assert new_word["id"] == word_id
    assert len(new_word["translations"]) == 1
    assert len(new_word["examples"]) == 1


def test_update_word(client, created_word, auth_headers):
    """Обновление слова"""
    response = created_word

    data = response.json()
    word_id = data["id"]

    response_update_word = client.put(
        f"/words/{word_id}",
        json={
            "word_en": "apple",
            "translations": [
                {
                    "translation_ru": "яблоко"
                },
                {
                    "translation_ru": "яблоня"
                },
            ],
            "examples": [
                {
                    "sentence": "I ate an apple"
                },
                {
                    "sentence": "It is an apple"
                }
            ]
        },
        headers=auth_headers
    )

    assert response_update_word.status_code == 200
    new_data = response_update_word.json()
    assert new_data["id"] == word_id
    assert len(new_data["translations"]) == 2
    assert len(new_data["examples"]) == 2


def test_delete_word(client, created_word, auth_headers):
    """Удаление слова"""
    response = created_word

    data = response.json()
    word_id = data["id"]

    response_delete_word = client.delete(
        f"/words/{word_id}",
        headers=auth_headers,
    )

    assert response_delete_word.status_code == 204

    response_get_word = client.get(
        f"/words/{word_id}",
        headers=auth_headers,
    )

    assert response_get_word.status_code == 404


def test_isolation(client, created_word, auth_headers_second):
    """Пользователь не может получить чужое слово"""

    response = created_word

    data = response.json()
    word_id = data["id"]

    response = client.get(
        f"/words/{word_id}",
        headers=auth_headers_second,
    )

    assert response.status_code == 404


def test_isolation_update(client, created_word, auth_headers_second):
    """Пользователь не может обновить чужое слово"""
    response = created_word

    data = response.json()
    word_id = data["id"]

    response_update = client.put(
        f"/words/{word_id}",
        json={
            "word_en": "hacked",
            "translations": [{"translation_ru": "взломано"}],
            "examples": [{"sentence": "hacked"}],
        },
        headers=auth_headers_second,
    )

    assert response_update.status_code == 404

def test_isolation_delete(client, created_word, auth_headers_second):
    """Пользователь не может удалить чужое слово"""
    response = created_word
    data = response.json()
    word_id = data["id"]

    response_delete = client.delete(
        f"/words/{word_id}",
        headers=auth_headers_second,
    )

    assert response_delete.status_code == 404


def test_update_status(client, created_word, auth_headers):
    """Успешная смена статуса слова"""
    word_id = created_word.json()["id"]

    response = client.patch(
        f"/words/{word_id}/status",
        json={
            "status": "learning"
        },
        headers=auth_headers,
    )

    data = response.json()
    assert response.status_code == 200
    assert data["progress"]["status"] == "learning"


def test_update_status_invalid(client, created_word, auth_headers):
    """Ошибка смены статуса с неизвестным значением"""
    word_id = created_word.json()["id"]

    response = client.patch(
        f"/words/{word_id}/status",
        json={
            "status": "invalid"
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_update_status_isolation(client, created_word, auth_headers_second):
    """Пользователь не может изменить статус чужого слова"""
    word_id = created_word.json()["id"]
    response = client.patch(
        f"/words/{word_id}/status",
        json={
            "status": "learning"
        },
        headers=auth_headers_second,
    )

    assert response.status_code == 404