# FastAPIのテスト
def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_applications(client):

    client.post(
        "/applications",
        json={
            "title": "出張申請",
            "content": "東京への出張申請です。",
        },
    )

    client.post(
        "/applications",
        json={
            "title": "備品購入申請",
            "content": "キーボード購入の申請です。",
        },
    )

    response = client.get("/applications")

    assert response.status_code == 200

    applications = response.json()
    assert len(applications) == 2
    assert applications[0]["title"] == "出張申請"
    assert applications[1]["title"] == "備品購入申請"


def test_get_application_by_id(client):
    created_response = client.post(
        "/applications",
        json={
            "title": "出張申請",
            "content": "東京への出張申請です。",
        },
    )

    application_id = created_response.json()["id"]

    response = client.get(f"/applications/{application_id}")

    assert response.status_code == 200
    application = response.json()
    assert application["id"] == 1
    assert application["title"] == "出張申請"


def test_get_application_by_id_not_found(client):
    response = client.get("/applications/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Application not found"}


def test_create_application(client):
    response = client.post(
        "/applications",
        json={"title": "新しい申請", "content": "新しい申請の内容です。"},
    )
    assert response.status_code == 201

    created_application = response.json()
    assert created_application["title"] == "新しい申請"
    assert created_application["content"] == "新しい申請の内容です。"
    assert created_application["status"] == "Pending"
