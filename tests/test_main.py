from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# FastAPIのテスト
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_applications():
    response = client.get("/applications")

    assert response.status_code == 200

    applications = response.json()
    assert len(applications) == 2
    assert applications[0]["title"] == "出張申請"
    assert applications[1]["title"] == "備品購入申請"

def test_get_application_by_id():
    response = client.get("/applications/1")

    assert response.status_code == 200
    application = response.json()
    assert application["id"] == 1
    assert application["title"] == "出張申請"

def test_get_application_by_id_not_found():
    response = client.get("/applications/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Application not found"}

def test_create_application():
    response = client.post("/applications", json={"title": "新しい申請", "content": "新しい申請の内容です。"})
    assert response.status_code == 201

    created_application = response.json()
    assert created_application["title"] == "新しい申請"
    assert created_application["content"] == "新しい申請の内容です。"
    assert created_application["status"] == "Pending"
