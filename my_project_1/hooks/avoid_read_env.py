import sys
import json

def main():
    #NOTE: read JSON data from stdin
    raw = sys.stdin.read()
    tool_args = json.loads(raw)

    #NOTE: extract the file path
    tool_input = tool_args.get("tool_input", {})
    read_path = tool_input.get("file_path")

    #NOTE: Check if Claude is trying to read the .env file
    if ".env" in read_path:
        print("You can not read the .env file", file=sys.stderr)
        sys.exit(2)    #NOTE: mục tiêu trả về 2 để block gọi tool

if __name__ == "__main__":
    main()