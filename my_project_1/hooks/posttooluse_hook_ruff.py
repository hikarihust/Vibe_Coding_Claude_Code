import sys
import json
import subprocess


def main():
    tool_args = json.loads(sys.stdin.read())
    file_path = tool_args.get("tool_input", {}).get("file_path") or ""

    if not file_path.endswith(".py"):
        sys.exit(0)  # Không phải Python file thì không làm gì

    result = subprocess.run(
        ["ruff", "check", "--fix", file_path],   # thêm "--fix" nếu muốn ruff tự sửa
        capture_output=True,
        text=True,
        encoding="utf-8",               # tránh lỗi cp932
        shell=False,
    )

    ########################
    #NOTE: tips/tricks để kiểm tra liệu hook có hoạt động chính xác hay không
    with open("hook_log_v3.txt", "w", encoding="utf-8") as myfile:
        myfile.write(f"Hook ran on: {file_path}:\n{result.stdout}")
    ########################

    if result.returncode != 0:
        # stderr + exit 2 => Claude nhận được feedback và sẽ tự sửa
        print(f"Ruff found issues in {file_path}:\n{result.stdout}", file=sys.stderr)
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
