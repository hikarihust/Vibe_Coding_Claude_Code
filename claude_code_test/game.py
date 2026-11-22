"""Game Búa - Bao - Kéo chơi với máy tính trên dòng lệnh.

Luật chơi:
    - Búa thắng Kéo (búa đập gãy kéo)
    - Kéo thắng Bao (kéo cắt bao)
    - Bao thắng Búa (bao bọc búa)
    - Hai bên ra giống nhau thì hòa.
"""

import random
import sys
import unicodedata
from dataclasses import dataclass
from enum import Enum


class LuaChon(Enum):
    """Các lựa chọn hợp lệ trong game."""

    BUA = "Búa"
    BAO = "Bao"
    KEO = "Kéo"


class KetQua(Enum):
    """Kết quả một ván, nhìn từ phía người chơi."""

    THANG = "Thắng"
    THUA = "Thua"
    HOA = "Hòa"


# Mỗi lựa chọn (key) thắng được lựa chọn tương ứng (value).
THANG_DUOC: dict[LuaChon, LuaChon] = {
    LuaChon.BUA: LuaChon.KEO,
    LuaChon.KEO: LuaChon.BAO,
    LuaChon.BAO: LuaChon.BUA,
}

# Các cách nhập được chấp nhận (đã chuẩn hóa: chữ thường, bỏ dấu).
BANG_NHAP: dict[str, LuaChon] = {
    "1": LuaChon.BUA,
    "bua": LuaChon.BUA,
    "2": LuaChon.BAO,
    "bao": LuaChon.BAO,
    "3": LuaChon.KEO,
    "keo": LuaChon.KEO,
}

LENH_THOAT: frozenset[str] = frozenset({"q", "quit", "exit", "thoat", "0"})

# Tạo sẵn một lần để không phải dựng lại list mỗi ván.
TAT_CA_LUA_CHON: tuple[LuaChon, ...] = tuple(LuaChon)


@dataclass
class BangDiem:
    """Lưu số ván thắng / thua / hòa của người chơi."""

    thang: int = 0
    thua: int = 0
    hoa: int = 0

    @property
    def tong_so_van(self) -> int:
        """Tổng số ván đã chơi."""
        return self.thang + self.thua + self.hoa

    def ghi_nhan(self, ket_qua: KetQua) -> None:
        """Cập nhật bảng điểm theo kết quả một ván."""
        if ket_qua is KetQua.THANG:
            self.thang += 1
        elif ket_qua is KetQua.THUA:
            self.thua += 1
        else:
            self.hoa += 1


def bo_dau(chuoi: str) -> str:
    """Bỏ dấu tiếng Việt, ví dụ: 'Kéo' -> 'Keo', 'Búa' -> 'Bua'."""
    chuoi = chuoi.replace("đ", "d").replace("Đ", "D")
    tach = unicodedata.normalize("NFD", chuoi)
    return "".join(ky_tu for ky_tu in tach if unicodedata.category(ky_tu) != "Mn")


def chuan_hoa(chuoi: str) -> str:
    """Chuẩn hóa chuỗi nhập: ký tự full-width -> ASCII (NFKC), bỏ khoảng trắng
    thừa, bỏ dấu, chữ thường.
    """
    return bo_dau(unicodedata.normalize("NFKC", chuoi).strip()).casefold()


def phan_tich_lua_chon(chuoi: str) -> LuaChon | None:
    """Chuyển chuỗi người dùng nhập thành LuaChon; trả về None nếu không hợp lệ."""
    return BANG_NHAP.get(chuan_hoa(chuoi))


def la_lenh_thoat(chuoi: str) -> bool:
    """Kiểm tra người dùng có muốn thoát game không."""
    return chuan_hoa(chuoi) in LENH_THOAT


def xac_dinh_ket_qua(nguoi_choi: LuaChon, may: LuaChon) -> KetQua:
    """Xác định kết quả ván đấu theo góc nhìn của người chơi."""
    if nguoi_choi is may:
        return KetQua.HOA
    if THANG_DUOC[nguoi_choi] is may:
        return KetQua.THANG
    return KetQua.THUA


def may_chon(rng: random.Random | None = None) -> LuaChon:
    """Máy chọn ngẫu nhiên một lựa chọn. Cho phép truyền rng để dễ kiểm thử."""
    nguon = rng if rng is not None else random
    return nguon.choice(TAT_CA_LUA_CHON)


def in_huong_dan() -> None:
    """In tiêu đề và hướng dẫn cách nhập."""
    print("=" * 40)
    print("      GAME BÚA - BAO - KÉO")
    print("=" * 40)
    print("Nhập lựa chọn của bạn:")
    print("  1 hoặc 'bua'  -> Búa")
    print("  2 hoặc 'bao'  -> Bao")
    print("  3 hoặc 'keo'  -> Kéo")
    print("  0 hoặc 'q'    -> Thoát")
    print("(Có thể gõ có dấu hoặc không dấu, hoa hay thường đều được.)")
    print("-" * 40)


def in_bang_diem(bang_diem: BangDiem) -> None:
    """In tỉ số hiện tại."""
    print(
        f"Tỉ số: Thắng {bang_diem.thang} | Thua {bang_diem.thua} | "
        f"Hòa {bang_diem.hoa} (Tổng {bang_diem.tong_so_van} ván)"
    )


def choi(rng: random.Random | None = None) -> BangDiem:
    """Vòng lặp chính của game. Trả về bảng điểm khi người chơi thoát."""
    bang_diem = BangDiem()
    in_huong_dan()

    while True:
        try:
            nhap = input("\nBạn chọn: ")
        except (EOFError, KeyboardInterrupt):
            print()  # Xuống dòng cho gọn khi bấm Ctrl+C / Ctrl+D.
            break

        if la_lenh_thoat(nhap):
            break

        nguoi_choi = phan_tich_lua_chon(nhap)
        if nguoi_choi is None:
            print("Lựa chọn không hợp lệ, vui lòng nhập 1, 2, 3 (hoặc 0 để thoát).")
            continue

        may = may_chon(rng)
        ket_qua = xac_dinh_ket_qua(nguoi_choi, may)
        bang_diem.ghi_nhan(ket_qua)

        print(f"Bạn ra: {nguoi_choi.value}  |  Máy ra: {may.value}")
        if ket_qua is KetQua.THANG:
            print(f">> Bạn THẮNG! {nguoi_choi.value} thắng {may.value}.")
        elif ket_qua is KetQua.THUA:
            print(f">> Bạn THUA! {may.value} thắng {nguoi_choi.value}.")
        else:
            print(">> HÒA!")
        in_bang_diem(bang_diem)

    print("\n===== KẾT THÚC GAME =====")
    in_bang_diem(bang_diem)
    print("Cảm ơn bạn đã chơi!")
    return bang_diem


def main() -> int:
    """Điểm vào chương trình.

    Console Windows thường dùng code page cũ (cp1252, cp932...) nên chuyển các
    luồng sang UTF-8 để in/nhập được tiếng Việt. errors="replace" giúp game không
    bị crash khi gặp byte không hợp lệ (dòng đó sẽ bị coi là lựa chọn sai).
    """
    for luong in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(luong, "reconfigure"):
            try:
                luong.reconfigure(encoding="utf-8", errors="replace")
            except (ValueError, OSError):
                pass
    choi()
    return 0


if __name__ == "__main__":
    sys.exit(main())
