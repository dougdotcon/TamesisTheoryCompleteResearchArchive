import json
from demonstrator_a_physical import verify_outputs
if __name__=="__main__":
    result=verify_outputs(); print(json.dumps(result,indent=2)); raise SystemExit(0 if result["valid"] else 1)
