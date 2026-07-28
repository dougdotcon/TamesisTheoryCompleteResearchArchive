from labctl import lean_check


if __name__ == "__main__":
    result = lean_check()
    print(result)
    raise SystemExit(0 if result["status"] == "PASS" else 1)
