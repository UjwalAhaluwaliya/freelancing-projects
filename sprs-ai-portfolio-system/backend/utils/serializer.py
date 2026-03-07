from bson import ObjectId
from datetime import datetime


def serialize_doc(doc):
    if doc is None:
        return None

    out = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            out[key] = str(value)
        elif isinstance(value, datetime):
            out[key] = value.isoformat() + "Z"
        elif isinstance(value, list):
            out[key] = [serialize_doc(item) if isinstance(item, dict) else str(item) if isinstance(item, ObjectId) else item for item in value]
        elif isinstance(value, dict):
            out[key] = serialize_doc(value)
        else:
            out[key] = value
    return out


def serialize_docs(docs):
    return [serialize_doc(doc) for doc in docs]
