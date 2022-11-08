import json

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.main import app
from app.db.base import Base
from app.db.session import engine
from app.dependencies import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

test_data = { 
    "isbn_valid": [ 
        "9780553593716",
        "9781608875337"
    ],
    "isbn_invalid": [
         "12345678",
         "1234567890123"
    ],
    "comments": [
        {
            "id": 1,
            "user": "first user",
            "body": "first comment"
        },
        {
            "id": 2,
            "user": "second user",
            "body": "second comment"
        }
    ]
}

def test_add_book():
    for isbn in test_data["isbn_valid"]:
        response = client.post("/books/{isbn}".format(isbn=isbn))
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["isbn"] == isbn
        assert "id" in data

    for isbn in test_data["isbn_valid"]:
        response = client.post("/books/{isbn}".format(isbn=isbn))
        assert response.status_code == 400, response.text
        data = response.json()
        assert data["detail"] == "Book already exists."

    for isbn in test_data["isbn_invalid"]:
        response = client.post("/books/{isbn}".format(isbn=isbn))
        assert response.status_code == 400, response.text

def test_update_book():
    for isbn in test_data["isbn_valid"]:
        response = client.put("/books/{isbn}".format(isbn=isbn))
        assert response.status_code == 200

    for isbn in test_data["isbn_invalid"]:
        response = client.put("/books/{isbn}".format(isbn=isbn))
        assert response.status_code == 400

def test_get_book():
    for isbn in test_data["isbn_valid"]:
        response = client.get("/books/{isbn}".format(isbn=isbn))
        assert response.status_code == 200
        data = response.json()
        assert data["isbn"] == isbn

    for isbn in test_data["isbn_invalid"]:
        response = client.get("/books/{isbn}".format(isbn=test_data["isbn_invalid"]))
        assert response.status_code == 400

    response = client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(test_data["isbn_valid"])

def test_add_comment():
    for comment in test_data["comments"]:
        response = client.post("/comments/{isbn}".format(isbn=test_data["isbn_valid"][0]), json.dumps(comment))
        assert response.status_code == 200
        response_body = response.json()
        assert response_body["id"] == comment["id"]
        assert response_body["user"] == comment["user"]
        assert response_body["body"] == comment["body"]

    for comment in test_data["comments"]:
        response = client.post("/comments/{isbn}".format(isbn=test_data["isbn_invalid"][0]), json.dumps(comment))
        assert response.status_code == 400

def test_get_comment():
    response = client.get("/comments/{isbn}".format(isbn=test_data["isbn_valid"][0]))
    assert response.status_code == 200
    response_body = response.json()
    for comment in response_body:
        comment_id = comment["id"] -1
        assert comment["id"] == test_data["comments"][comment_id]["id"]
        assert comment["user"] == test_data["comments"][comment_id]["user"]
        assert comment["body"] == test_data["comments"][comment_id]["body"]

    response = client.get("/comments/{isbn}".format(isbn=test_data["isbn_invalid"][0]))
    assert response.status_code == 400

def test_update_comment():
    comment = test_data["comments"][0]
    update_body = { "body": "update first comment" }
    response = client.put("/comments/{comment_id}".format(comment_id=comment["id"]), json.dumps(update_body))
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["id"] == comment["id"]
    assert response_body["user"] == comment["user"]
    assert response_body["body"] == update_body["body"]

    response = client.put("/comments/{comment_id}".format(comment_id=999),json.dumps(update_body))
    assert response.status_code == 400

def test_delete_comment():
    comment = test_data["comments"][0]
    response = client.delete("/comments/{comment_id}".format(comment_id=comment["id"]))
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["id"] == comment["id"]

    response = client.delete("/comments/{comment_id}".format(comment_id=comment["id"]))
    assert response.status_code == 400

def test_delete_book():
    for isbn in test_data["isbn_valid"]:
        response = client.delete("/books/{isbn}".format(isbn=isbn))
        assert response.status_code == 200

    for isbn in test_data["isbn_invalid"]:
        response = client.delete("/books/{isbn}".format(isbn=isbn))
        assert response.status_code == 400