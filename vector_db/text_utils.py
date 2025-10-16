import numbers
import json
from datetime import datetime
from config import CHUNK_SIZE

structured_field_keywords = ["id", "uid", "employeeID", "shiftType", "tax", "bankAccount", "email"]


def is_embeddable(field_name, value):
    """
    Returns True if the field should be embedded:
    - Skip booleans, numbers, datetimes, None
    - Skip structured fields identified by keywords in their name
    """
    if value is None:
        return False
    if isinstance(value, (bool, numbers.Number, datetime)):
        return False
    if any(keyword.lower() in field_name.lower() for keyword in structured_field_keywords):
        return False
    return True


def extract_text(data, depth=0, max_depth=4):
    """Recursively extract all textual fields with max depth."""
    if depth > max_depth:
        if isinstance(data, (dict, list)):
            return [json.dumps(data, ensure_ascii=False)]
        return []

    text_chunks = []
    if isinstance(data, dict):
        for v in data.values():
            if is_embeddable(v):
                text_chunks.extend(extract_text(v, depth + 1, max_depth))
    elif isinstance(data, list):
        for item in data:
            if is_embeddable(item):
                text_chunks.extend(extract_text(item, depth + 1, max_depth))
    elif isinstance(data, str) and data.strip():
        text_chunks.append(data.strip())
    return text_chunks

def chunk_text(text, chunk_size=CHUNK_SIZE):
    tokens = text.split()
    return [" ".join(tokens[i:i + chunk_size]) for i in range(0, len(tokens), chunk_size)]
