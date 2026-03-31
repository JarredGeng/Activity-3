"""
Authentication helpers: validate login credentials using the database layer.
"""

from __future__ import annotations

from typing import Any, Optional

from db import get_user_by_username, is_manager_role, verify_password


def authenticate(username: str, password: str) -> Optional[dict[str, Any]]:
    """
    Verify username/password against the database.

    Returns a safe user dict (no password) on success, or None on failure.
    """
    username = (username or "").strip()
    if not username or not password:
        return None

    user = get_user_by_username(username)
    if not user:
        return None

    if not verify_password(user["password"], password):
        return None

    return {"id": user["id"], "username": user["username"], "role": user["role"]}


def verify_manager_credentials(username: str, password: str) -> bool:
    """
    Used when creating an account from the login screen: require a valid
    manager or owner account to authorize the action.
    """
    user = authenticate(username, password)
    if not user:
        return False
    return is_manager_role(user["role"])
