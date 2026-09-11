"""SQLite store adapter (v1). JSON-document-column tables + generated columns +
uniqueness/append-only constraints, per docs/promotion_storage_design.md.

Records are canonical JSON in the `doc` column; generated columns exist only for
the fields we query/constrain. The adapter is the only module that touches SQL, so
a future PostgreSQL move changes only this file.
"""
import sqlite3
from contextlib import contextmanager

DDL = [
    """CREATE TABLE IF NOT EXISTS source_candidate (
        candidate_id     TEXT PRIMARY KEY,
        doc              TEXT NOT NULL,
        canonical_url    TEXT GENERATED ALWAYS AS (json_extract(doc,'$.canonical_url')) VIRTUAL,
        promotion_status TEXT GENERATED ALWAYS AS (json_extract(doc,'$.promotion.promotion_status')) VIRTUAL,
        review_status    TEXT GENERATED ALWAYS AS (json_extract(doc,'$.review.review_status')) VIRTUAL,
        dedupe_status    TEXT GENERATED ALWAYS AS (json_extract(doc,'$.dedupe.dedupe_status')) VIRTUAL
    )""",
    """CREATE TABLE IF NOT EXISTS source (
        source_id          TEXT PRIMARY KEY,
        doc                TEXT NOT NULL,
        canonical_url      TEXT GENERATED ALWAYS AS (json_extract(doc,'$.canonical_url')) STORED,
        active_status      TEXT GENERATED ALWAYS AS (json_extract(doc,'$.active_status')) VIRTUAL,
        review_status      TEXT GENERATED ALWAYS AS (json_extract(doc,'$.review_status')) VIRTUAL,
        collection_allowed INTEGER GENERATED ALWAYS AS (json_extract(doc,'$.collection_allowed')) VIRTUAL
    )""",
    # dedupe guarantee: at most one registry Source per normalized URL
    "CREATE UNIQUE INDEX IF NOT EXISTS idx_source_canonical_url ON source(canonical_url)",
    """CREATE TABLE IF NOT EXISTS promotion_event (
        seq                  INTEGER PRIMARY KEY,           -- authoritative monotonic sequence
        event_id             TEXT NOT NULL UNIQUE,
        doc                  TEXT NOT NULL,
        promotion_attempt_id TEXT    GENERATED ALWAYS AS (json_extract(doc,'$.promotion_attempt_id')) VIRTUAL,
        attempt_generation   INTEGER GENERATED ALWAYS AS (json_extract(doc,'$.attempt_generation')) VIRTUAL,
        candidate_id         TEXT    GENERATED ALWAYS AS (json_extract(doc,'$.candidate_id')) VIRTUAL,
        event_status         TEXT    GENERATED ALWAYS AS (json_extract(doc,'$.event_status')) VIRTUAL
    )""",
    # promotion_event is append-only (immutable audit)
    "CREATE TRIGGER IF NOT EXISTS promotion_event_no_update BEFORE UPDATE ON promotion_event "
    "BEGIN SELECT RAISE(ABORT,'promotion_event is append-only'); END",
    "CREATE TRIGGER IF NOT EXISTS promotion_event_no_delete BEFORE DELETE ON promotion_event "
    "BEGIN SELECT RAISE(ABORT,'promotion_event is append-only'); END",
    """CREATE TABLE IF NOT EXISTS source_candidate_link (
        source_id    TEXT NOT NULL REFERENCES source(source_id),
        candidate_id TEXT NOT NULL REFERENCES source_candidate(candidate_id),
        linked_at    TEXT NOT NULL,
        PRIMARY KEY (source_id, candidate_id)
    )""",
    "CREATE INDEX IF NOT EXISTS idx_link_candidate ON source_candidate_link(candidate_id)",
]


def connect(path):
    # isolation_level=None => autocommit; we manage write transactions explicitly
    # with BEGIN IMMEDIATE (see immediate_txn).
    conn = sqlite3.connect(path, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def init_schema(conn):
    for stmt in DDL:
        conn.execute(stmt)


def safe_rollback(conn):
    """Roll back if a transaction is open; ignore 'no active transaction'."""
    try:
        conn.execute("ROLLBACK")
    except sqlite3.OperationalError:
        pass


@contextmanager
def immediate_txn(conn):
    """Acquire the write lock up front (BEGIN IMMEDIATE); commit on success,
    roll back on ANY failure of the body OR of the commit itself.

    Guarding COMMIT matters: under WAL a commit can fail (SQLITE_BUSY from a
    reader blocking checkpoint, SQLITE_IOERR, disk-full). If unguarded, SQLite
    leaves the transaction OPEN and the write lock held, which would poison the
    connection and mask the real error. Here a failed commit is rolled back and
    the original exception re-raised, so the transaction is always closed."""
    conn.execute("BEGIN IMMEDIATE")
    try:
        yield
    except BaseException:
        safe_rollback(conn)
        raise
    else:
        try:
            conn.execute("COMMIT")
        except BaseException:
            safe_rollback(conn)
            raise
