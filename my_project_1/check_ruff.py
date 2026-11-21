"""Tạo 2 numpy arrays có phụ thuộc gần tuyến tính và vẽ bằng matplotlib."""

import os  # Cố ý import nhưng không sử dụng để test PostToolUse hook (ruff F401)

import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    rng = np.random.default_rng(seed=42)

    # x: 100 điểm cách đều trong [0, 10]
    x = np.linspace(0, 10, 100)

    # y = 2.5 * x + 1.0 + nhiễu Gaussian -> phụ thuộc gần tuyến tính
    noise = rng.normal(loc=0.0, scale=1.5, size=x.shape)
    y = 2.5 * x + 1.0 + noise

    # Ước lượng đường hồi quy tuyến tính
    slope, intercept = np.polyfit(x, y, deg=1)
    corr = np.corrcoef(x, y)[0, 1]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(x, y, s=20, alpha=0.7, label="Dữ liệu (x, y)")
    ax.plot(
        x,
        slope * x + intercept,
        color="red",
        linewidth=2,
        label=f"Hồi quy: y = {slope:.2f}x + {intercept:.2f}",
    )
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"Phụ thuộc gần tuyến tính giữa x và y (r = {corr:.3f})")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
