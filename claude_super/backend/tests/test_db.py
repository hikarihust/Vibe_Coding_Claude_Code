import pytest
from app import db


@pytest.fixture
def conn(tmp_path):
    with db.connect(tmp_path / "t.db") as c:
        db.init_db(c)
        yield c


def test_make_title_collapses_whitespace_and_cuts_20():
    assert db.make_title("  Giải thích\n\n  closure   trong JavaScript ") == "Giải thích closure t"


def test_make_title_vietnamese():
    t = db.make_title("Tiếng Việt có dấu đầy đủ ở đây")
    assert t == "Tiếng Việt có dấu đầ" and len(t) == 20


def test_list_sessions_newest_activity_first(conn):
    a = db.create_session(conn, "A")
    b = db.create_session(conn, "B")
    db.add_message(conn, a["id"], "user", "hi")
    assert [s["title"] for s in db.list_sessions(conn)] == ["A", "B"]


def test_messages_in_order(conn):
    s = db.create_session(conn, "S")
    db.add_message(conn, s["id"], "user", "q")
    db.add_message(conn, s["id"], "assistant", "a")
    assert [(m["role"], m["content"]) for m in db.list_messages(conn, s["id"])] == [("user", "q"), ("assistant", "a")]


def test_rename_and_missing(conn):
    s = db.create_session(conn, "old")
    assert db.rename_session(conn, s["id"], "new")["title"] == "new"
    assert db.rename_session(conn, 999, "x") is None
    assert db.get_session(conn, 999) is None


def test_delete_cascades_messages(conn):
    s = db.create_session(conn, "S")
    db.add_message(conn, s["id"], "user", "q")
    assert db.delete_session(conn, s["id"]) is True
    assert db.list_messages(conn, s["id"]) == []
    assert conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0] == 0
    assert db.delete_session(conn, s["id"]) is False
