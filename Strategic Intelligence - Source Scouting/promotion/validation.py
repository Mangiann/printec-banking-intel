"""JSON Schema validation contracts (Draft 2020-12, format-checked).

The JSON Schemas remain the canonical record contracts; records are validated in
code BEFORE any insert/update (storage design section 10). DB constraints are the
second enforcement layer.
"""
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

SCHEMA_FILES = {
    "source_candidate": "source_candidate.schema.json",
    "source": "source_registry.schema.json",
    "promotion_event": "promotion_event.schema.json",
}


class ValidationError(Exception):
    pass


def load_validators(schemas_dir):
    fc = FormatChecker()
    validators = {}
    for name, fn in SCHEMA_FILES.items():
        schema = json.loads((Path(schemas_dir) / fn).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validators[name] = Draft202012Validator(schema, format_checker=fc)
    return validators


def validate(validators, name, record):
    v = validators[name]
    errs = sorted(v.iter_errors(record), key=lambda e: list(e.path))
    if errs:
        msgs = ["/".join(map(str, e.path)) or "<root>"
                for e in errs[:6]]
        detail = " | ".join(f"{p}: {e.message}" for p, e in zip(msgs, errs[:6]))
        raise ValidationError(f"{name} schema-invalid: {detail}")
