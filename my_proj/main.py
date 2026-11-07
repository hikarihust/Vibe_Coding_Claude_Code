import shutil
from pathlib import Path


def add(a, b):
    """Trả về tổng của hai số a và b."""
    return a + b


def subtract(a: int, b: int) -> int:
    """Trả về hiệu của hai số nguyên a và b (a - b)."""
    return a - b


def copy_folder(src: str, dst: str, overwrite: bool = True) -> int:
    """Copy toàn bộ file (kể cả thư mục con) từ folder src sang folder dst.

    - Giữ nguyên cấu trúc thư mục con.
    - Tự tạo folder dst nếu chưa tồn tại.
    - overwrite=False: bỏ qua các file đã tồn tại ở dst.

    Trả về số lượng file đã copy.
    """
    src_path = Path(src)
    dst_path = Path(dst)

    if not src_path.is_dir():
        raise NotADirectoryError(f"Folder nguồn không tồn tại: {src_path}")
    if dst_path.resolve().is_relative_to(src_path.resolve()):
        raise ValueError("Folder đích không được nằm bên trong folder nguồn.")

    copied = 0
    for file in src_path.rglob("*"):
        if not file.is_file():
            continue
        target = dst_path / file.relative_to(src_path)
        if target.exists() and not overwrite:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file, target)  # copy2 giữ cả metadata (thời gian sửa đổi...)
        copied += 1

    return copied


if __name__ == "__main__":
    print(add(3, 5))  # 8
    print(subtract(10, 4))  # 6
