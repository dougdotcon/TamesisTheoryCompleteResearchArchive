from labctl import validate


if __name__ == "__main__":
    result = validate()
    print({"claim_count": result["claim_count"], "errors": result["errors"]})
    raise SystemExit(0 if not result["errors"] else 1)
