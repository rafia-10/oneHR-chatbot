import numbers
from datetime import datetime
from firebase_connect import db_dev, db_internal

id_keywords = ["id", "uid", "employeeid", "account", "email", "tax"]

def extract_structured(data, parent_key=""):
    structured = {}

    if isinstance(data, dict):
        for k, v in data.items():
            key_path = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, (numbers.Number, bool, datetime)):
                structured[key_path] = v
            elif isinstance(v, str) and any(substr in k.lower() for substr in id_keywords):
                structured[key_path] = v
            elif isinstance(v, (dict, list)):
                structured.update(extract_structured(v, key_path))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            key_path = f"{parent_key}[{i}]" if parent_key else str(i)
            structured.update(extract_structured(item, key_path))

    return structured
