from labctl import validate


if __name__ == "__main__":
    result = validate()
    print(result["status"])
    raise SystemExit(0 if result["status"] == "PASS" else 1)
