"""Deterministic utilities: stable serialization, content hashing, ids, timestamps."""
import hashlib
import json
import uuid
from datetime import datetime, timezone


def now_iso():
    """RFC 3339 / ISO 8601 UTC timestamp, second precision, 'Z' suffix."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def new_id(prefix):
    return f"{prefix}_{uuid.uuid4().hex}"


def canonical_json(obj):
    """Stable serialization used BOTH for storage and for content hashing.

    Sorted keys + compact separators => deterministic bytes, so before/after
    content hashes are comparable across processes (storage design section 11/13).
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def content_hash(obj):
    return "sha256:" + hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()
