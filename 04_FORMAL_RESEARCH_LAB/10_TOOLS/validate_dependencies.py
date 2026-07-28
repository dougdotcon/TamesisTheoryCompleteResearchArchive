from labctl import validate


if __name__ == "__main__":
    result = validate()
    raise SystemExit(0 if not result["errors"] else 1)
