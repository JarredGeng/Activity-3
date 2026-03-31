"""
SQLite database layer for the Store GUI application.
Handles schema, migrations, password hashing, and user queries.
"""

from __future__ import annotations

import hashlib
import os
import secrets
import sqlite3
from typing import Any, Optional

# Project root directory (where store.db lives)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "store.db")

# PBKDF2 parameters for password storage (stdlib only)
_PBKDF2_ITERATIONS = 120_000


def _hash_password(plain: str) -> str:
    """Return a salted PBKDF2 hash string: 'salt_hex$hash_hex'."""
    salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac(
        "sha256",
        plain.encode("utf-8"),
        salt,
        _PBKDF2_ITERATIONS,
    )
    return f"{salt.hex()}${dk.hex()}"


def verify_password(stored: str, plain: str) -> bool:
    """Check plain password against stored 'salt$hash' string."""
    try:
        salt_hex, hash_hex = stored.split("$", 1)
        salt = bytes.fromhex(salt_hex)
        dk = hashlib.pbkdf2_hmac(
            "sha256",
            plain.encode("utf-8"),
            salt,
            _PBKDF2_ITERATIONS,
        )
        return dk.hex() == hash_hex
    except (ValueError, AttributeError):
        return False


def get_connection() -> sqlite3.Connection:
    """Open a SQLite connection with row factory for dict-like rows."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create tables if they do not exist and seed demo users."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK (role IN ('employee', 'manager', 'owner'))
            )
            """
        )
        conn.commit()

    _seed_if_empty()


def _seed_if_empty() -> None:
    """Insert demo manager and employee accounts when the users table is empty."""
    with get_connection() as conn:
        row = conn.execute("SELECT COUNT(*) AS c FROM users").fetchone()
        if row and row["c"] > 0:
            return

        # Default passwords for class demos (change in production)
        manager_pw = _hash_password("manager123")
        employee_pw = _hash_password("employee123")

        conn.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("manager", manager_pw, "manager"),
        )
        conn.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("employee", employee_pw, "employee"),
        )
        conn.commit()


def get_user_by_username(username: str) -> Optional[dict[str, Any]]:
    """Fetch one user by username, or None if not found."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, username, password, role FROM users WHERE username = ?",
            (username.strip(),),
        ).fetchone()
        return dict(row) if row else None


def list_usernames_matching(prefix: str, limit: int = 20) -> list[str]:
    """
    Return usernames that start with the given prefix (case-insensitive).
    Used for login autocomplete suggestions.
    """
    prefix = prefix.strip()
    if not prefix:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT username FROM users ORDER BY username LIMIT ?",
                (limit,),
            ).fetchall()
        return [r["username"] for r in rows]

    like = prefix + "%"
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT username FROM users
            WHERE username LIKE ? COLLATE NOCASE
            ORDER BY username
            LIMIT ?
            """,
            (like, limit),
        ).fetchall()
    return [r["username"] for r in rows]


def username_exists(username: str) -> bool:
    """Return True if username is already taken."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM users WHERE username = ? COLLATE NOCASE",
            (username.strip(),),
        ).fetchone()
    return row is not None


def create_user(username: str, password: str, role: str) -> None:
    """Insert a new user. Raises sqlite3.IntegrityError on duplicate username."""
    hashed = _hash_password(password)
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username.strip(), hashed, role),
        )
        conn.commit()


def is_manager_role(role: str) -> bool:
    """Managers and owners may create accounts."""
    return role in ("manager", "owner")
