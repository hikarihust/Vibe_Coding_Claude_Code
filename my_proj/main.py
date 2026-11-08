def tinh_tong(*so):
    """Tính tổng của các số được truyền vào.

    Args:
        *so (int | float): Một hoặc nhiều số cần tính tổng.

    Returns:
        int | float: Tổng của tất cả các số. Trả về 0 nếu không truyền số nào.

    Examples:
        >>> tinh_tong(1, 2, 3)
        6
        >>> tinh_tong(1.5, 2.5)
        4.0
        >>> tinh_tong()
        0
    """
    return sum(so)


if __name__ == "__main__":
    print(tinh_tong(1, 2))
