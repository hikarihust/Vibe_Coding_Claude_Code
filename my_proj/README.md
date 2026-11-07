# my_proj

Project Python nhỏ gồm các hàm tiện ích trong file [main.py](main.py): hai hàm tính toán cơ bản và một hàm copy toàn bộ file từ folder này sang folder khác.

## Yêu cầu

- Python **3.9 trở lên** (hàm `copy_folder` dùng `Path.is_relative_to`, có từ Python 3.9).
- Không cần cài thêm thư viện. Chỉ dùng thư viện chuẩn `shutil` và `pathlib`.

## Chạy thử

```bash
python main.py
```

Kết quả:

```
8
6
```

## Giải thích code

### Import

```python
import shutil
from pathlib import Path
```

- `shutil`: dùng để copy file (`shutil.copy2`).
- `pathlib.Path`: xử lý đường dẫn theo kiểu hướng đối tượng, chạy được trên cả Windows lẫn Linux/macOS.

### `add(a, b)`

```python
def add(a, b):
    return a + b
```

Trả về tổng của `a` và `b`. Hàm không khai báo kiểu, nên dùng được với số nguyên, số thực, hoặc bất kỳ kiểu nào hỗ trợ toán tử `+`.

Ví dụ: `add(3, 5)` → `8`.

### `subtract(a: int, b: int) -> int`

```python
def subtract(a: int, b: int) -> int:
    return a - b
```

Trả về hiệu `a - b`. Phần `a: int, b: int -> int` là *type hint*: nó giúp IDE (Pylance) gợi ý và cảnh báo khi truyền sai kiểu, nhưng Python không bắt buộc kiểu lúc chạy.

Ví dụ: `subtract(10, 4)` → `6`.

### `copy_folder(src, dst, overwrite=True) -> int`

Copy toàn bộ file, kể cả file trong các thư mục con, từ folder `src` sang folder `dst`, rồi trả về số file đã copy.

| Tham số     | Kiểu   | Ý nghĩa                                                              |
|-------------|--------|----------------------------------------------------------------------|
| `src`       | `str`  | Đường dẫn folder nguồn                                               |
| `dst`       | `str`  | Đường dẫn folder đích (tự tạo nếu chưa có)                           |
| `overwrite` | `bool` | `True` (mặc định): ghi đè file trùng tên. `False`: bỏ qua file đã có |

Hàm chạy theo các bước sau:

1. **Chuyển đường dẫn sang `Path`**
   ```python
   src_path = Path(src)
   dst_path = Path(dst)
   ```

2. **Kiểm tra đầu vào**
   ```python
   if not src_path.is_dir():
       raise NotADirectoryError(...)
   if dst_path.resolve().is_relative_to(src_path.resolve()):
       raise ValueError(...)
   ```
   - Báo lỗi nếu folder nguồn không tồn tại hoặc không phải là folder.
   - Báo lỗi nếu folder đích nằm *bên trong* folder nguồn. Nếu không chặn, file vừa copy sang sẽ lại bị duyệt và copy tiếp, gây lặp vô hạn. `resolve()` đổi đường dẫn thành đường dẫn tuyệt đối để so sánh cho chính xác.

3. **Duyệt mọi file trong folder nguồn**
   ```python
   for file in src_path.rglob("*"):
       if not file.is_file():
           continue
   ```
   `rglob("*")` duyệt đệ quy toàn bộ cây thư mục. Các mục là thư mục thì bỏ qua, vì thư mục đích sẽ được tạo ở bước 5.

4. **Tính đường dẫn đích, giữ nguyên cấu trúc thư mục**
   ```python
   target = dst_path / file.relative_to(src_path)
   ```
   Ví dụ: `src/sub/b.txt` → phần tương đối là `sub/b.txt` → đích là `dst/sub/b.txt`.

5. **Bỏ qua file đã có (nếu không ghi đè), tạo thư mục cha rồi copy**
   ```python
   if target.exists() and not overwrite:
       continue
   target.parent.mkdir(parents=True, exist_ok=True)
   shutil.copy2(file, target)
   copied += 1
   ```
   - `mkdir(parents=True, exist_ok=True)` tạo cả chuỗi thư mục cha và không báo lỗi nếu thư mục đã tồn tại.
   - `shutil.copy2` copy nội dung **và** metadata, ví dụ thời gian sửa đổi. Nếu chỉ dùng `shutil.copy` thì metadata không được giữ lại.

6. **Trả về số file đã copy** (`return copied`).

Ví dụ sử dụng:

```python
from main import copy_folder

so_file = copy_folder("folder_nguon", "folder_dich")
print(f"Đã copy {so_file} file")

# Không ghi đè file đã tồn tại ở folder đích
copy_folder("folder_nguon", "folder_dich", overwrite=False)
```

### Khối `if __name__ == "__main__":`

```python
if __name__ == "__main__":
    print(add(3, 5))       # 8
    print(subtract(10, 4)) # 6
```

Đoạn code này chỉ chạy khi thực thi trực tiếp `python main.py`. Khi file được `import` từ file khác, ví dụ `from main import copy_folder`, đoạn này **không** chạy.
