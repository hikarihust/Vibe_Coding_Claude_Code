# AI Coding's Chatbot

Web app chat cá nhân dùng Ollama (`gemma4:31b-cloud`), lưu lịch sử hội thoại vào SQLite.

- Backend: FastAPI — `backend/`
- Frontend: React + TypeScript + Vite + Tailwind CSS — `frontend/`
- Thiết kế: `docs/superpowers/specs/2026-11-22-chatbot-design.md`

## Yêu cầu

- [Ollama](https://ollama.com) đã cài và đang chạy (`http://localhost:11434`)
- Đã đăng nhập Ollama để dùng model cloud: `ollama signin`
- Python 3.13, Node.js 20+

## Chạy backend (cổng 8000)

```bash
cd backend
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt   # macOS/Linux: .venv/bin/python
.venv/Scripts/python -m uvicorn app.main:app --port 8000 --reload
```

Database được tạo tự động tại `backend/chat.db`. Xoá file này để xoá toàn bộ lịch sử.

## Chạy frontend (cổng 5173)

```bash
cd frontend
npm install
npm run dev
```

Mở http://localhost:5173. Vite chuyển các request `/api` sang backend ở cổng 8000.

## Chạy test backend

```bash
cd backend
.venv/Scripts/python -m pytest
```

## Lỗi thường gặp

- **"Không kết nối được Ollama…"**: Ollama chưa chạy hoặc chưa `ollama signin`.
