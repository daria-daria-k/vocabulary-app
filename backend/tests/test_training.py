def test_get_next_en_ru(client, created_word, auth_headers):
    """Тренировка EN→RU показывает английское слово"""
    response = client.get("/training/next?direction=en_ru", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "apple"
    assert data["direction"] == "en_ru"


def test_get_next_ru_en(client, created_word, auth_headers):
    """Тренировка RU→EN показывает русский перевод"""
    response = client.get("/training/next?direction=ru_en", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["question"] == "яблоко"


def test_get_next_no_words(client, auth_headers):
    """Нет слов для тренировки → 404"""
    response = client.get("/training/next?direction=en_ru", headers=auth_headers)
    assert response.status_code == 404


def test_answer_correct(client, created_word, auth_headers):
    """Верный перевод засчитывается"""
    word_id = created_word.json()["id"]
    response = client.post(
        "/training/answer",
        json={"word_id": word_id, "direction": "en_ru", "answer": "яблоко"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["correct"] is True


def test_answer_wrong(client, created_word, auth_headers):
    """Неверный перевод не засчитывается"""
    word_id = created_word.json()["id"]
    response = client.post(
        "/training/answer",
        json={"word_id": word_id, "direction": "en_ru", "answer": "берёза"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["correct"] is False


def test_normalize_answer_correct(client, created_word, auth_headers):
    """Верный нормализированный перевод засчитывается"""
    word_id = created_word.json()["id"]
    response = client.post(
        "/training/answer",
        json={"word_id": word_id, "direction": "en_ru", "answer": " ЯБЛОКО "},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["correct"] is True


def test_answer_empty(client, created_word, auth_headers):
    """Пустой ответ отклоняется с 422"""
    word_id = created_word.json()["id"]
    response = client.post(
        "/training/answer",
        json={"word_id": word_id, "direction": "en_ru", "answer": "   "},
        headers=auth_headers,
    )
    assert response.status_code == 422


def test_answer_isolated(client, created_word, auth_headers_second):
    word_id = created_word.json()["id"]
    response = client.post(
        "/training/answer",
        json={"word_id": word_id, "direction": "en_ru", "answer": "яблоко"},
        headers=auth_headers_second,
    )

    assert response.status_code == 404
