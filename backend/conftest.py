from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db

import os
from dotenv import load_dotenv

import pytest

from fastapi.testclient import TestClient
from app.main import app
from app.redis_client import redis_client

load_dotenv()

DATABASE_URL_TEST = os.getenv('DATABASE_URL_TEST')
engine = create_engine(DATABASE_URL_TEST, echo=True)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def test_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def client(test_db):
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def user_data():
    return {
        "email": "test@mail.ru",
        "password": "test123",
    }


@pytest.fixture
def registered_user(client, user_data):
    client.post("/auth/register", json=user_data)

    return user_data


@pytest.fixture
def auth_headers(client, registered_user):
    response = client.post(
        "/auth/login",
        json=registered_user)

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def created_word(client, auth_headers):
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
        headers=auth_headers
    )
    return response

@pytest.fixture
def auth_headers_second(client):
    """Заголовки авторизации для второго пользователя (для тестов изоляции)"""
    other_user = {"email": "other@mail.ru", "password": "test123"}
    client.post(
        "/auth/register",
        json=other_user,
    )
    login = client.post(
        "/auth/login",
        json=other_user
    )
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def clear_redis(autouse=True):
    redis_client.flushdb()
    yield