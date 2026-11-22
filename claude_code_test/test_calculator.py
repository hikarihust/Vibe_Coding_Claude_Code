"""Unit test cho calculator.py."""

import math

import pytest

import calculator
from calculator import chia, chia_lay_du, cong, dinh_dang, nhan, nhap_so, tinh, tru


# ---------- 5 phép toán cơ bản ----------

@pytest.mark.parametrize(
    ("ham", "a", "b", "ky_vong"),
    [
        (cong, 7, 3, 10),
        (cong, -1.5, 0.5, -1.0),
        (tru, 7, 3, 4),
        (tru, 3, 7, -4),
        (nhan, 7, 3, 21),
        (nhan, -2, 0.5, -1.0),
        (chia, 7, 2, 3.5),
        (chia, -9, 3, -3),
        (chia_lay_du, 7, 3, 1),
        (chia_lay_du, 7.5, 2, 1.5),
    ],
)
def test_phep_toan(ham, a, b, ky_vong):
    assert ham(a, b) == pytest.approx(ky_vong)


def test_chia_lay_du_so_am_theo_dau_so_chia():
    assert chia_lay_du(-7, 3) == 2
    assert chia_lay_du(7, -3) == -2


@pytest.mark.parametrize("ham", [chia, chia_lay_du])
@pytest.mark.parametrize("so_chia", [0, 0.0, -0.0])
def test_chia_cho_0_bao_loi(ham, so_chia):
    with pytest.raises(ZeroDivisionError):
        ham(1, so_chia)


# ---------- tinh() ----------

def test_tinh_theo_ky_hieu():
    assert tinh("+", 2, 3) == 5
    assert tinh("/", 1, 4) == 0.25


def test_tinh_ky_hieu_khong_hop_le():
    with pytest.raises(KeyError):
        tinh("^", 2, 3)


def test_tinh_tran_so_bao_loi():
    with pytest.raises(OverflowError):
        tinh("*", 1e308, 10)


# ---------- dinh_dang() ----------

@pytest.mark.parametrize(
    ("x", "ky_vong"),
    [
        (10.0, "10"),
        (-4.0, "-4"),
        (123456790.0, "123456790"),
        (3.5, "3.5"),
        (1 / 3, "0.3333333333333333"),
    ],
)
def test_dinh_dang(x, ky_vong):
    assert dinh_dang(x) == ky_vong


# ---------- nhap_so() ----------

def _gia_lap_input(monkeypatch, cac_gia_tri):
    du_lieu = iter(cac_gia_tri)
    monkeypatch.setattr("builtins.input", lambda _="": next(du_lieu))


def test_nhap_so_hop_le(monkeypatch):
    _gia_lap_input(monkeypatch, ["5"])
    assert nhap_so("> ") == 5.0


def test_nhap_so_bo_qua_gia_tri_sai(monkeypatch, capsys):
    _gia_lap_input(monkeypatch, ["abc", "", "2.5"])
    assert nhap_so("> ") == 2.5
    assert capsys.readouterr().out.count("không hợp lệ") == 2


@pytest.mark.parametrize("gia_tri", ["inf", "-inf", "nan", "1e400"])
def test_nhap_so_tu_choi_so_khong_huu_han(monkeypatch, capsys, gia_tri):
    _gia_lap_input(monkeypatch, [gia_tri, "1"])
    assert nhap_so("> ") == 1.0
    assert "hữu hạn" in capsys.readouterr().out


# ---------- main() ----------

def test_main_tinh_va_thoat(monkeypatch, capsys):
    _gia_lap_input(monkeypatch, ["+", "123456789", "1", "/", "5", "0", "x", "q"])
    calculator.main()
    out = capsys.readouterr().out
    assert "123456789 + 1 = 123456790" in out
    assert "Không thể chia cho 0" in out
    assert "Lựa chọn không hợp lệ" in out
    assert "Tạm biệt!" in out


def test_phep_toan_day_du():
    assert set(calculator.PHEP_TOAN) == {"+", "-", "*", "/", "%"}
    assert all(callable(ham) for _, ham in calculator.PHEP_TOAN.values())
    assert not math.isnan(tinh("%", 7, 3))
