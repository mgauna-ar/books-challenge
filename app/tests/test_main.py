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
    "isbn_valid": "9780073545776",
    "isbn_invalid": "12345678",
    "comment_add": { "user": "test", "body": "test comment"},
    "comment_update": { "body": "comment_update" },
    "comment_id": 1
}

def test_add_book():
    response = client.post("/books/{isbn}".format(isbn=test_data["isbn_valid"]))
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["isbn"] == test_data["isbn_valid"]
    assert "id" in data

    response = client.post("/books/{isbn}".format(isbn=test_data["isbn_valid"]))
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Book already exists."

    response = client.post("/books/{isbn}".format(isbn=test_data["isbn_invalid"]))
    assert response.status_code == 400, response.text

def test_update_book():
    response = client.put("/books/{isbn}".format(isbn=test_data["isbn_valid"]))
    assert response.status_code == 200

    response = client.put("/books/{isbn}".format(isbn=test_data["isbn_invalid"]))
    assert response.status_code == 400

def test_get_book():
    response = client.get("/books/{isbn}".format(isbn=test_data["isbn_valid"]))
    assert response.status_code == 200
    data = response.json()
    assert data["isbn"] == test_data["isbn_valid"]

    response = client.get("/books/{isbn}".format(isbn=test_data["isbn_invalid"]))
    assert response.status_code == 400

    response = client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

def test_add_comment():
    response = client.post("/comments/{isbn}".format(isbn=test_data["isbn_valid"]), json.dumps(test_data["comment_add"]))
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["id"] == test_data["comment_id"]
    assert response_body["user"] == test_data["comment_add"]["user"]
    assert response_body["body"] == test_data["comment_add"]["body"]

    response = client.post("/comments/{isbn}".format(isbn=test_data["isbn_invalid"]), json.dumps(test_data["comment_add"]))
    assert response.status_code == 400

def test_get_comment():
    response = client.get("/comments/{isbn}".format(isbn=test_data["isbn_valid"]))
    assert response.status_code == 200
    response_body = response.json()
    assert response_body[0]["id"] == test_data["comment_id"]
    assert response_body[0]["user"] == test_data["comment_add"]["user"]
    assert response_body[0]["body"] == test_data["comment_add"]["body"]

    response = client.get("/comments/{isbn}".format(isbn=test_data["isbn_invalid"]))
    assert response.status_code == 400

def test_update_comment():
    response = client.put("/comments/{comment_id}".format(comment_id=test_data["comment_id"]), json.dumps(test_data["comment_update"]))
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["id"] == test_data["comment_id"]
    assert response_body["user"] == test_data["comment_add"]["user"]
    assert response_body["body"] == test_data["comment_update"]["body"]

    response = client.put("/comments/{comment_id}".format(comment_id=2),json.dumps(test_data["comment_update"]))
    assert response.status_code == 400

def test_delete_comment():
    response = client.delete("/comments/{comment_id}".format(comment_id=test_data["comment_id"]))
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["id"] == test_data["comment_id"]

    response = client.delete("/comments/{comment_id}".format(comment_id=test_data["comment_id"]))
    assert response.status_code == 400

def test_delete_book():
    response = client.delete("/books/{isbn}".format(isbn=test_data["isbn_valid"]))
    assert response.status_code == 200

    response = client.delete("/books/{isbn}".format(isbn=test_data["isbn_invalid"]))
    assert response.status_code == 400