"""
Login screen: username (with autocomplete), password, Login and Create Account.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING, Callable, Optional

import db

if TYPE_CHECKING:
    from main import StoreApp


class LoginScreen(ttk.Frame):
    """First screen: validate credentials and route to dashboards."""

    def __init__(
        self,
        parent: tk.Widget,
        app: "StoreApp",
        *,
        on_login_success: Callable[[dict], None],
        on_open_create_account: Callable[[], None],
    ) -> None:
        super().__init__(parent)
        self._app = app
        self._on_login_success = on_login_success
        self._on_open_create_account = on_open_create_account

        self._username_var = tk.StringVar()
        self._password_var = tk.StringVar()

        self._build_ui()

    def _build_ui(self) -> None:
        pad = {"padx": 12, "pady": 8}

        title = ttk.Label(self, text="Store Management — Sign in", font=("Segoe UI", 16, "bold"))
        title.pack(pady=(24, 8))

        form = ttk.Frame(self)
        form.pack(padx=40, pady=12)

        ttk.Label(form, text="Username").grid(row=0, column=0, sticky="w", **pad)
        # Combobox allows typing and selecting suggestions from the database
        self._user_combo = ttk.Combobox(
            form,
            textvariable=self._username_var,
            width=32,
        )
        self._user_combo.grid(row=0, column=1, **pad)
        self._user_combo.bind("<KeyRelease>", self._on_username_key)
        self._user_combo.bind("<<ComboboxSelected>>", self._on_username_key)

        ttk.Label(form, text="Password").grid(row=1, column=0, sticky="w", **pad)
        self._pwd_entry = ttk.Entry(form, textvariable=self._password_var, width=34, show="•")
        self._pwd_entry.grid(row=1, column=1, **pad)

        btn_row = ttk.Frame(self)
        btn_row.pack(pady=16)
        ttk.Button(btn_row, text="Login", command=self._try_login).pack(side=tk.LEFT, padx=8)
        ttk.Button(btn_row, text="Create Account", command=self._on_open_create_account).pack(
            side=tk.LEFT, padx=8
        )

        self._status = ttk.Label(self, text="", foreground="#c0392b")
        self._status.pack(pady=4)

        self._refresh_username_suggestions()

    def _on_username_key(self, _event: Optional[tk.Event] = None) -> None:
        """Update combobox values from DB as the user types."""
        self._refresh_username_suggestions()

    def _refresh_username_suggestions(self) -> None:
        prefix = self._username_var.get()
        try:
            names = db.list_usernames_matching(prefix)
        except OSError as e:
            self._status.config(text=f"Database error: {e}")
            return
        self._user_combo["values"] = names

    def _try_login(self) -> None:
        from auth import authenticate

        user = self._username_var.get().strip()
        pwd = self._password_var.get()

        self._status.config(text="")
        if not user or not pwd:
            self._status.config(text="Enter both username and password.")
            return

        result = authenticate(user, pwd)
        if not result:
            self._status.config(text="Invalid username or password.")
            return

        self._password_var.set("")
        self._on_login_success(result)
