import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  title       TEXT NOT NULL,
  created_at  TEXT NOT NULL,
  updated_at  TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS messages (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id  INTEGER NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
  role        TEXT NOT NULL CHECK (role IN ('user','assistant')),
  content     TEXT NOT NULL,
  created_at  TEXT NOT NULL
);
"""

SESSION_COLS = "id, title, updated_at"
MESSAGE_COLS = "id, role, content, created_at"


@contextmanager
def connect(db_path: Path) -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(db_path)
    try:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        # Tạo lại bảng nếu chat.db bị xoá trong lúc backend đang chạy.
        init_db(conn)
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_title(text: str) -> str:
    return " ".join(text.split())[:20]


def get_session(conn: sqlite3.Connection, session_id: int) -> dict | None:
    row = conn.execute(f"SELECT {SESSION_COLS} FROM sessions WHERE id = ?", (session_id,)).fetchone()
    return dict(row) if row else None


def create_session(conn: sqlite3.Connection, title: str) -> dict:
    now = _now()
    cur = conn.execute(
        "INSERT INTO sessions (title, created_at, updated_at) VALUES (?, ?, ?)", (title, now, now)
    )
    return get_session(conn, cur.lastrowid)


def list_sessions(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute(f"SELECT {SESSION_COLS} FROM sessions ORDER BY updated_at DESC, id DESC")
    return [dict(r) for r in rows]


def rename_session(conn: sqlite3.Connection, session_id: int, title: str) -> dict | None:
    conn.execute("UPDATE sessions SET title = ? WHERE id = ?", (title, session_id))
    return get_session(conn, session_id)


def delete_session(conn: sqlite3.Connection, session_id: int) -> bool:
    return conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,)).rowcount > 0


def add_message(conn: sqlite3.Connection, session_id: int, role: str, content: str) -> dict:
    now = _now()
    cur = conn.execute(
        "INSERT INTO messages (session_id, role, content, created_at) VALUES (?, ?, ?, ?)",
        (session_id, role, content, now),
    )
    conn.execute("UPDATE sessions SET updated_at = ? WHERE id = ?", (now, session_id))
    row = conn.execute(f"SELECT {MESSAGE_COLS} FROM messages WHERE id = ?", (cur.lastrowid,)).fetchone()
    return dict(row)


def list_messages(conn: sqlite3.Connection, session_id: int) -> list[dict]:
    rows = conn.execute(
        f"SELECT {MESSAGE_COLS} FROM messages WHERE session_id = ? ORDER BY id", (session_id,)
    )
    return [dict(r) for r in rows]
