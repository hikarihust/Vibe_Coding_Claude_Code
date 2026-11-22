"""Chương trình máy tính đơn giản với 5 phép toán cơ bản:
cộng, trừ, nhân, chia và chia lấy dư.
"""

import math
import sys
from typing import Callable

PhepToan = Callable[[float, float], float]


def cong(a: float, b: float) -> float:
    """Phép cộng."""
    return a + b


def tru(a: float, b: float) -> float:
    """Phép trừ."""
    return a - b


def nhan(a: float, b: float) -> float:
    """Phép nhân."""
    return a * b


def chia(a: float, b: float) -> float:
    """Phép chia. Báo lỗi nếu chia cho 0."""
    if b == 0:
        raise ZeroDivisionError("Không thể chia cho 0")
    return a / b


def chia_lay_du(a: float, b: float) -> float:
    """Phép chia lấy dư theo quy ước của Python (giống hàm MOD của Excel).

    Kết quả luôn cùng dấu với số chia b, ví dụ: -7 % 3 = 2 và 7 % -3 = -2.
    Báo lỗi nếu chia cho 0.
    """
    if b == 0:
        raise ZeroDivisionError("Không thể chia lấy dư cho 0")
    return a % b


PHEP_TOAN: dict[str, tuple[str, PhepToan]] = {
    "+": ("Cộng", cong),
    "-": ("Trừ", tru),
    "*": ("Nhân", nhan),
    "/": ("Chia", chia),
    "%": ("Chia lấy dư", chia_lay_du),
}


def tinh(ky_hieu: str, a: float, b: float) -> float:
    """Thực hiện phép toán theo ký hiệu.

    Raises:
        KeyError: nếu ký hiệu không hợp lệ.
        ZeroDivisionError: nếu chia hoặc chia lấy dư cho 0.
        OverflowError: nếu kết quả vượt quá giới hạn số thực.
    """
    _, ham = PHEP_TOAN[ky_hieu]
    ket_qua = ham(a, b)
    if not math.isfinite(ket_qua):
        raise OverflowError("Kết quả quá lớn, vượt quá giới hạn tính toán")
    return ket_qua


def dinh_dang(x: float) -> str:
    """Định dạng số: số nguyên in không có '.0', số thực in đầy đủ chữ số."""
    if x.is_integer():
        return str(int(x))
    return repr(x)


def nhap_so(thong_bao: str) -> float:
    """Yêu cầu người dùng nhập số hữu hạn cho đến khi hợp lệ."""
    while True:
        try:
            so = float(input(thong_bao))
        except ValueError:
            print("Giá trị không hợp lệ, vui lòng nhập lại một số.")
            continue
        if not math.isfinite(so):
            print("Vui lòng nhập một số hữu hạn.")
            continue
        return so


def main() -> None:
    """Vòng lặp chính: hiển thị menu, đọc lựa chọn và in kết quả."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print("=== MÁY TÍNH 5 PHÉP TOÁN CƠ BẢN ===")
    while True:
        print("\nCác phép toán:")
        for ky_hieu, (ten, _) in PHEP_TOAN.items():
            print(f"  {ky_hieu}  : {ten}")
        print("  q  : Thoát")

        lua_chon = input("Chọn phép toán: ").strip()
        if lua_chon.lower() == "q":
            print("Tạm biệt!")
            break
        if lua_chon not in PHEP_TOAN:
            print("Lựa chọn không hợp lệ.")
            continue

        a = nhap_so("Nhập số thứ nhất: ")
        b = nhap_so("Nhập số thứ hai: ")

        ten, _ = PHEP_TOAN[lua_chon]
        try:
            ket_qua = tinh(lua_chon, a, b)
        except (ZeroDivisionError, OverflowError) as loi:
            print(f"Lỗi: {loi}")
            continue
        print(
            f"Kết quả ({ten}): {dinh_dang(a)} {lua_chon} {dinh_dang(b)}"
            f" = {dinh_dang(ket_qua)}"
        )


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nTạm biệt!")
