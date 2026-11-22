# AI Coding's Chatbot — Design

Ngày: 2026-11-22
Yêu cầu gốc: `PROMPT.md`

## 1. Mục đích

Một web app chat cá nhân để người dùng hỏi đáp hằng ngày với LLM `gemma4:31b-cloud` chạy qua Ollama. Hội thoại được lưu lại theo session để có thể mở lại và chat tiếp bất cứ lúc nào. Chỉ có một người dùng, chạy trên máy local.

## 2. Mục tiêu / Không làm / Thất bại nếu

**Mục tiêu**
- Chat với model, câu trả lời hiện dần từng chữ (streaming).
- Sidebar liệt kê các session đã lưu; click để load lại hội thoại và chat tiếp.
- Tạo chat mới, đổi tên, xoá session.
- Có lựa chọn dark mode và light mode với mặc định là light mode
- Có thiết kế responsive

**Không làm (non-goals)**
- User / đăng nhập / phân quyền.
- Chọn nhiều model, chỉnh tham số model, system prompt tuỳ chỉnh.
- Sửa / regenerate tin nhắn, tìm kiếm session, upload file.
- Deploy, Docker, tối ưu cho mobile.

**Thất bại nếu (anti-goals)**
- Mất lịch sử hội thoại (tin nhắn đã hiển thị là xong nhưng không có trong DB khi load lại).
- Sidebar đầy các session rỗng do bấm "New Chat" nhiều lần.
- Màn hình đứng im không phản hồi trong lúc model đang trả lời.

## 3. Ràng buộc (do người dùng quyết định)

- Frontend: React + TypeScript + Vite, CSS bằng Tailwind CSS.
- Backend: FastAPI (Python).
- Database: SQLite.
- LLM: Ollama, model `gemma4:31b-cloud`. Model `-cloud` cần Ollama đã cài và đã `ollama signin`.
- Tiêu đề chung: "AI Coding's Chatbot".
- Tên session = prompt đầu tiên của user trong session, giới hạn 20 ký tự.
- Dấu "..." cạnh tên session chỉ hiện khi hover, mở ra 2 hành động: đổi tên, xoá.
- Nút "New Chat" nằm trên cùng sidebar.

Môi trường máy: Node 26, Python 3.13, Windows.

## 4. Các cách tiếp cận đã cân nhắc

| Cách | Mô tả | Đánh đổi |
|---|---|---|
| **A. Streaming qua HTTP (đã chọn)** | Backend gọi Ollama với `stream=True`, trả về `StreamingResponse`; frontend đọc bằng `fetch` + `ReadableStream`, nối dần vào tin nhắn. | Thêm ~30–40 dòng code, phải xử lý huỷ khi đổi session. Đổi lại thấy chữ hiện ngay — quan trọng vì model 31B qua cloud có thể chậm. |
| B. Request/response thường | Một API trả JSON khi model trả lời xong, hiện "đang trả lời…". | Đơn giản nhất nhưng chờ lâu không thấy gì. |
| C. WebSocket | Kênh hai chiều. | Phức tạp hơn mà không thêm lợi ích cho một user, một luồng chat. Loại. |

Người dùng chọn **A**.

## 5. Thiết kế

### 5.1 Cấu trúc thư mục

```
claude_super/
  backend/
    app/
      main.py        # FastAPI app, routes
      db.py          # SQLite: kết nối, tạo bảng, truy vấn
      llm.py         # gọi Ollama (stream)
    tests/
    requirements.txt
  frontend/          # Vite React-TS + Tailwind
```

### 5.2 Database (SQLite, file `backend/chat.db`)

```sql
CREATE TABLE sessions (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  title       TEXT NOT NULL,
  created_at  TEXT NOT NULL,   -- ISO 8601 UTC
  updated_at  TEXT NOT NULL
);

CREATE TABLE messages (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id  INTEGER NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
  role        TEXT NOT NULL CHECK (role IN ('user','assistant')),
  content     TEXT NOT NULL,
  created_at  TEXT NOT NULL
);
```

- Dùng module `sqlite3` chuẩn của Python, bật `PRAGMA foreign_keys = ON` mỗi kết nối. Không dùng ORM (quyết định của Claude: 2 bảng, không cần).
- Bảng được tạo tự động khi backend khởi động.
- `updated_at` của session được cập nhật mỗi khi có tin nhắn mới → sidebar sắp xếp theo `updated_at` giảm dần (session vừa chat nổi lên đầu).

### 5.3 API (prefix `/api`)

| Method | Path | Body | Trả về |
|---|---|---|---|
| GET | `/api/sessions` | – | `[{id, title, updated_at}]`, mới nhất trước |
| POST | `/api/sessions` | `{first_message}` | `{id, title, updated_at}` — tạo session, title = 20 ký tự đầu |
| GET | `/api/sessions/{id}/messages` | – | `[{id, role, content, created_at}]` theo thứ tự thời gian |
| POST | `/api/sessions/{id}/messages` | `{content}` | **Stream** `text/plain; charset=utf-8` — các đoạn chữ của câu trả lời |
| PATCH | `/api/sessions/{id}` | `{title}` | session đã cập nhật |
| DELETE | `/api/sessions/{id}` | – | 204 |

Session không tồn tại → 404. `content`/`title` rỗng sau khi trim → 422.

**Luồng gửi tin nhắn (`POST /api/sessions/{id}/messages`):**
1. Lưu tin nhắn user vào DB ngay (không mất câu hỏi dù model lỗi).
2. Lấy toàn bộ lịch sử session (user + assistant), gửi cho Ollama `chat(model, messages, stream=True)`. Không cắt bớt lịch sử.
3. Stream từng đoạn `content` về client, đồng thời gom vào buffer.
4. Stream xong → lưu tin nhắn assistant đầy đủ, cập nhật `updated_at`.
5. Nếu Ollama lỗi hoặc client ngắt kết nối giữa chừng → **không lưu** câu trả lời dở dang (quyết định của Claude). Nếu lỗi xảy ra trước khi có đoạn chữ nào → trả HTTP 502 kèm thông báo. Nếu lỗi giữa stream → đóng stream; frontend coi stream kết thúc bất thường là lỗi.

**Tên session:** `first_message` → gộp mọi khoảng trắng/xuống dòng liên tiếp thành 1 dấu cách, trim, lấy 20 ký tự đầu. Không thêm "…" vào dữ liệu; nếu cần, UI tự cắt hiển thị bằng CSS.

**Ollama:** dùng thư viện Python `ollama` (`AsyncClient`), host mặc định `http://localhost:11434`. Tên model là hằng số trong `llm.py`. Không system prompt.

### 5.4 Frontend

```
┌──────────────────────────────────────────────────────────┐
│ AI Coding's Chatbot                                       │
├───────────────┬──────────────────────────────────────────┤
│ [+ New Chat]  │                                          │
│               │   (user)      Giải thích closure trong JS│
│ Giải thích cl…│                                          │
│ Viết hàm sort ⋯│  (bot) Closure là ...  ```js ... ```    │
│ Hỏi về Docker │                                          │
│               ├──────────────────────────────────────────┤
│               │ ┌──────────────────────────────┐ [Send]  │
│               │ │ textarea nhiều dòng          │         │
│               │ └──────────────────────────────┘         │
└───────────────┴──────────────────────────────────────────┘
```

- **Header** chứa tiêu đề "AI Coding's Chatbot".
- **Sidebar trái** (rộng cố định, cuộn riêng): nút "New Chat" trên cùng; danh sách session; session đang mở được highlight.
  - Hover vào một dòng → hiện nút "...". Click → menu nhỏ: "Đổi tên", "Xoá".
  - Đổi tên: tên biến thành ô input tại chỗ; Enter lưu, Esc huỷ, blur lưu. Tên rỗng → không lưu.
  - Xoá: `window.confirm` xác nhận. Nếu xoá session đang mở → về màn hình chat mới.
- **New Chat:** chỉ xoá trắng khung chat và bỏ chọn session ở sidebar; **không** tạo gì trong DB. Session chỉ được tạo khi gửi tin nhắn đầu tiên (tránh session rỗng).
- **Khung chat:** tin nhắn user căn phải, assistant căn trái. Assistant render Markdown (`react-markdown` + `remark-gfm`, code block có tô màu cú pháp, ví dụ `rehype-highlight`). Tự cuộn xuống cuối khi có chữ mới. Khung chat mới chưa có tin nhắn hiện một dòng chào ngắn.
- **Ô nhập:** textarea nhiều dòng, tự giãn chiều cao đến một mức tối đa rồi cuộn. **Enter gửi, Shift+Enter xuống dòng.** Nút "Send" và Enter bị vô hiệu khi ô trống hoặc đang chờ trả lời.
- **Gửi tin nhắn:**
  1. Nếu chưa có session → `POST /api/sessions` lấy id, thêm vào đầu sidebar, chọn nó.
  2. Hiện ngay tin nhắn user + một tin nhắn assistant rỗng (hiệu ứng đang gõ).
  3. `POST .../messages`, đọc stream, nối chữ vào tin nhắn assistant.
  4. Xong → làm mới danh sách session (thứ tự theo `updated_at`).
- **Đổi session / New Chat khi đang stream:** huỷ request bằng `AbortController`, rồi load session mới. Câu trả lời dở dang bị bỏ (khớp với backend không lưu).
- **Lỗi:** hiện dòng báo lỗi màu đỏ trong khung chat ở vị trí câu trả lời (ví dụ "Không kết nối được Ollama"). Tin nhắn user vẫn còn (đã lưu ở backend).
- **State:** `useState` trong `App` là đủ; không dùng thư viện quản lý state (quyết định của Claude).
- **Dev:** Vite proxy `/api` → `http://localhost:8000`, nên không cần cấu hình CORS.

### 5.5 Giao diện / màu sắc

Dùng bảng màu trong `design-system-DESIGN.md` (đề xuất của Claude, người dùng chưa phản đối): màu chính `#6c4cf2` (hover `#5638d6`) cho nút Send / New Chat / bubble user; dải neutral `#f7f7f8`–`#17181b` cho nền, viền, chữ; danger `#e5484d` cho lỗi và hành động Xoá. Khai báo làm theme color của Tailwind. Font Inter (cho chữ) và JetBrains Mono (cho code). Chỉ giao diện sáng. Khoảng cách theo lưới 4px/8px.

### 5.6 Kiểm thử

- Backend: pytest + FastAPI `TestClient`, Ollama được mock. Test CRUD session, cắt tên 20 ký tự, cascade xoá messages, luồng stream lưu đủ user + assistant, lỗi Ollama không lưu assistant.
- Frontend: kiểm tra thủ công trên trình duyệt (gửi, stream, đổi session giữa chừng, đổi tên, xoá, reload trang vẫn còn lịch sử).

6. Thông tin bổ sung
- Dùng `sqlite3` và `ollama` Python.
- Các phần sau bạn tự quyết:
  - Chia component React cụ thể, tên file, cách tổ chức hook.
  - Phiên bản thư viện, cách cài Tailwind (khuyến nghị Tailwind v4 với plugin `@tailwindcss/vite`).
  - Chi tiết visual: kích thước, bo góc, icon "...", hiệu ứng đang gõ.
