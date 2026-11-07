def add(a, b):
    """Trả về tổng của hai số a và b."""
    return a + b


def subtract(a: int, b: int) -> int:
    """Trả về hiệu của hai số nguyên a và b (a - b)."""
    return a - b


if __name__ == "__main__":
    print(add(3, 5))  # 8
    print(subtract(10, 4))  # 6
