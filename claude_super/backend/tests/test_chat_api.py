import pytest

from app import llm


def fake(chunks, fail_at=None, calls=None):
    async def _stream(messages):
        if calls is not None:
            calls.append(messages)
        for i, c in enumerate(chunks):
            if i == fail_at:
                raise RuntimeError("ollama down")
            yield c
        if fail_at == len(chunks):
            raise RuntimeError("ollama down")

    return _stream


def new_session(client):
    return client.post("/api/sessions", json={"first_message": "q"}).json()["id"]


def msgs(client, sid):
    return [(m["role"], m["content"]) for m in client.get(f"/api/sessions/{sid}/messages").json()]


def test_stream_saves_user_and_assistant(client, monkeypatch):
    calls = []
    monkeypatch.setattr(llm, "stream_chat", fake(["Xin ", "chào"], calls=calls))
    sid = new_session(client)
    r = client.post(f"/api/sessions/{sid}/messages", json={"content": "hi"})
    assert r.status_code == 200 and r.text == "Xin chào"
    assert r.headers["content-type"].startswith("text/plain")
    assert msgs(client, sid) == [("user", "hi"), ("assistant", "Xin chào")]
    assert calls[0] == [{"role": "user", "content": "hi"}]


def test_full_history_sent(client, monkeypatch):
    calls = []
    monkeypatch.setattr(llm, "stream_chat", fake(["a"], calls=calls))
    sid = new_session(client)
    client.post(f"/api/sessions/{sid}/messages", json={"content": "1"})
    client.post(f"/api/sessions/{sid}/messages", json={"content": "2"})
    assert [m["content"] for m in calls[1]] == ["1", "a", "2"]


def test_stream_vietnamese_roundtrip(client, monkeypatch):
    monkeypatch.setattr(llm, "stream_chat", fake(["Đây là ", "tiếng Việt 🙂"]))
    sid = new_session(client)
    assert client.post(f"/api/sessions/{sid}/messages", json={"content": "x"}).text == "Đây là tiếng Việt 🙂"


def test_ollama_down_returns_502_and_keeps_user_message(client, monkeypatch):
    monkeypatch.setattr(llm, "stream_chat", fake([], fail_at=0))
    sid = new_session(client)
    r = client.post(f"/api/sessions/{sid}/messages", json={"content": "hi"})
    assert r.status_code == 502 and "Ollama" in r.json()["detail"]
    assert msgs(client, sid) == [("user", "hi")]


def test_mid_stream_error_not_saved(client, monkeypatch):
    monkeypatch.setattr(llm, "stream_chat", fake(["part"], fail_at=1))
    sid = new_session(client)
    with pytest.raises(RuntimeError):
        client.post(f"/api/sessions/{sid}/messages", json={"content": "hi"})
    assert msgs(client, sid) == [("user", "hi")]


def test_send_updates_session_order(client, monkeypatch):
    monkeypatch.setattr(llm, "stream_chat", fake(["a"]))
    a = new_session(client)
    b = new_session(client)
    client.post(f"/api/sessions/{a}/messages", json={"content": "x"})
    assert [s["id"] for s in client.get("/api/sessions").json()] == [a, b]


def test_blank_content_422(client):
    sid = new_session(client)
    assert client.post(f"/api/sessions/{sid}/messages", json={"content": "  \n"}).status_code == 422


def test_send_to_missing_session_404(client):
    assert client.post("/api/sessions/999/messages", json={"content": "x"}).status_code == 404
