# Plan: FastAPI Items app (Pydantic v2)

## Context
Bài thực hành dùng context7 plugin để viết FastAPI app đơn giản với 3 endpoint CRUD cho items.
Thư mục `claude_plugin/` hiện chỉ có `.claude/settings.json` → tạo mới hoàn toàn.
Đã tra context7 (`/websites/fastapi_tiangolo`): dùng `response_model`, `status_code=status.HTTP_201_CREATED`,
`responses={404: {"model": Message}}` + `HTTPException` cho 404.

## Files sẽ tạo (trong `claude_plugin/`)
1. `main.py`
   - Models Pydantic v2:
     - `ItemCreate(BaseModel)`: `name: str = Field(min_length=1)`, `description: str | None = None`, `price: float = Field(gt=0)`
     - `Item(ItemCreate)`: thêm `id: int`
   - Storage in-memory: `items_db: dict[int, Item]`, counter `next_id` (dùng `itertools.count(1)`)
   - `GET /items` → `response_model=list[Item]`, trả `list(items_db.values())`
   - `POST /items` → `status_code=201`, `response_model=Item`; tạo `Item(id=..., **payload.model_dump())` (API v2: `model_dump`)
   - `GET /items/{item_id}` (`item_id: int`) → `response_model=Item`, `responses={404: ...}`; không có → `raise HTTPException(404, "Item not found")`
2. `requirements.txt`: `fastapi[standard]>=0.115`, `pydantic>=2`
3. `test_main.py`: dùng `fastapi.testclient.TestClient` + pytest — test list rỗng, tạo item (201), get theo id, get id không tồn tại (404), validate lỗi (422).

## Verification
- `pip install -r requirements.txt pytest`
- `pytest -q` → tất cả pass
- `fastapi dev main.py` → mở http://127.0.0.1:8000/docs thử 3 endpoint
