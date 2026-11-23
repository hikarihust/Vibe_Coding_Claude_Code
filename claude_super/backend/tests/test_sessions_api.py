from fastapi.testclient import TestClient

from app.main import create_app


def test_recovers_when_db_file_deleted_while_running(tmp_path):
    path = tmp_path / "chat.db"
    client = TestClient(create_app(path))
    path.unlink()  # người dùng xoá chat.db khi backend đang chạy
    assert client.get("/api/sessions").status_code == 200
    assert client.post("/api/sessions", json={"first_message": "x"}).status_code == 200


def test_create_list_get_messages(client):
    r = client.post("/api/sessions", json={"first_message": "Giải thích closure trong JavaScript"})
    assert r.status_code == 200
    s = r.json()
    assert s["title"] == "Giải thích closure t"
    assert client.get("/api/sessions").json() == [s]
    assert client.get(f"/api/sessions/{s['id']}/messages").json() == []  # first_message không được lưu


def test_rename(client):
    sid = client.post("/api/sessions", json={"first_message": "x"}).json()["id"]
    r = client.patch(f"/api/sessions/{sid}", json={"title": "  Tên mới  "})
    assert r.status_code == 200 and r.json()["title"] == "Tên mới"


def test_delete(client):
    sid = client.post("/api/sessions", json={"first_message": "x"}).json()["id"]
    assert client.delete(f"/api/sessions/{sid}").status_code == 204
    assert client.get("/api/sessions").json() == []


def test_missing_session_404(client):
    assert client.get("/api/sessions/999/messages").status_code == 404
    assert client.patch("/api/sessions/999", json={"title": "a"}).status_code == 404
    assert client.delete("/api/sessions/999").status_code == 404


def test_blank_title_422(client):
    assert client.post("/api/sessions", json={"first_message": " \n "}).status_code == 422
    sid = client.post("/api/sessions", json={"first_message": "x"}).json()["id"]
    assert client.patch(f"/api/sessions/{sid}", json={"title": "   "}).status_code == 422
