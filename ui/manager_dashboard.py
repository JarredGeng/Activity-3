"""
Manager / owner dashboard: includes navigation to Create Account.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from main import StoreApp


class ManagerDashboard(ttk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        app: "StoreApp",
        *,
        on_logout: Callable[[], None],
        on_create_account: Callable[[], None],
    ) -> None:
        super().__init__(parent)
        self._app = app
        self._on_logout = on_logout
        self._on_create_account = on_create_account
        self._build_ui()

    def _build_ui(self) -> None:
        header = ttk.Frame(self)
        header.pack(fill=tk.X, padx=16, pady=12)
        ttk.Label(header, text="Manager Dashboard", font=("Segoe UI", 18, "bold")).pack(
            side=tk.LEFT
        )
        ttk.Button(header, text="Log out", command=self._on_logout).pack(side=tk.RIGHT)

        body = ttk.Frame(self)
        body.pack(fill=tk.BOTH, expand=True, padx=24, pady=16)

        role = self._app.current_user["role"] if self._app.current_user else ""
        ttk.Label(
            body,
            text=f"Signed in as {self._app.current_user['username']} ({role}).",
        ).pack(anchor="w", pady=(0, 12))

        ttk.Label(
            body,
            text="Use Create Account to add employees, managers, or owners.",
            justify=tk.LEFT,
        ).pack(anchor="w", pady=(0, 16))

        ttk.Button(body, text="Create Account", command=self._on_create_account).pack(anchor="w")
