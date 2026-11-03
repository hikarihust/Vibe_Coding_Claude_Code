def find_max(a: int, b: int) -> int:
    """Trả về giá trị lớn nhất giữa hai số nguyên a và b."""
    return a if a >= b else b


if __name__ == "__main__":
    print(find_max(3, 7))   # 7
    print(find_max(-5, -2)) # -2
    print(find_max(4, 4))   # 4
