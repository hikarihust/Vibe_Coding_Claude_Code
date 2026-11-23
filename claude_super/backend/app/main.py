from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, StringConstraints

from app import db

NonBlank = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class SessionCreate(BaseModel):
    first_message: NonBlank


class SessionRename(BaseModel):
    title: NonBlank


class MessageCreate(BaseModel):
    content: NonBlank


def _not_found() -> HTTPException:
    return HTTPException(404, "Session not found")


def create_app(db_path: Path) -> FastAPI:
    with db.connect(db_path) as conn:
        db.init_db(conn)

    app = FastAPI(title="AI Coding's Chatbot")

    @app.get("/api/sessions")
    def list_sessions():
        with db.connect(db_path) as conn:
            return db.list_sessions(conn)

    @app.post("/api/sessions")
    def create_session(body: SessionCreate):
        with db.connect(db_path) as conn:
            return db.create_session(conn, db.make_title(body.first_message))

    @app.get("/api/sessions/{session_id}/messages")
    def list_messages(session_id: int):
        with db.connect(db_path) as conn:
            if db.get_session(conn, session_id) is None:
                raise _not_found()
            return db.list_messages(conn, session_id)

    @app.patch("/api/sessions/{session_id}")
    def rename_session(session_id: int, body: SessionRename):
        with db.connect(db_path) as conn:
            session = db.rename_session(conn, session_id, body.title)
        if session is None:
            raise _not_found()
        return session

    @app.delete("/api/sessions/{session_id}", status_code=204)
    def delete_session(session_id: int):
        with db.connect(db_path) as conn:
            if not db.delete_session(conn, session_id):
                raise _not_found()
        return Response(status_code=204)

    return app


app = create_app(Path(__file__).resolve().parent.parent / "chat.db")
