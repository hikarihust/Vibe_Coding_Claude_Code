from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, StringConstraints

from app import db, llm

OLLAMA_ERROR = "Không kết nối được Ollama. Kiểm tra Ollama đang chạy và đã `ollama signin`."

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

    @app.post("/api/sessions/{session_id}/messages")
    async def send_message(session_id: int, body: MessageCreate):
        with db.connect(db_path) as conn:
            if db.get_session(conn, session_id) is None:
                raise _not_found()
            db.add_message(conn, session_id, "user", body.content)
            history = [
                {"role": m["role"], "content": m["content"]}
                for m in db.list_messages(conn, session_id)
            ]

        stream = llm.stream_chat(history)
        try:
            first = await anext(stream)
        except StopAsyncIteration:
            first = ""
        except Exception:
            raise HTTPException(502, OLLAMA_ERROR)

        async def body_stream():
            parts = [first]
            yield first
            # Lỗi giữa chừng hoặc client ngắt kết nối: exception thoát ra, không lưu câu trả lời dở.
            async for chunk in stream:
                parts.append(chunk)
                yield chunk
            with db.connect(db_path) as conn:
                db.add_message(conn, session_id, "assistant", "".join(parts))

        return StreamingResponse(body_stream(), media_type="text/plain; charset=utf-8")

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
