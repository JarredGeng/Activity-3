"""
Create user account form (manager/owner only).

When opened from the login screen, manager credentials must be supplied to authorize.
When opened from the manager dashboard, the logged-in user is already verified.
"""

from __future__ import annotations

import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from typing import TYPE_CHECKING, Callable

import db
from auth import verify_manager_credentials

if TYPE_CHECKING:
    from main import StoreApp


class CreateAccountScreen(ttk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        app: "StoreApp",
        *,
        require_manager_auth: bool,
        on_back: Callable[[], None],
        on_account_created: Callable[[], None],
    ) -> None:
        super().__init__(parent)
        self._app = app
        self._require_manager_auth = require_manager_auth
        self._on_back = on_back
        self._on_account_created = on_account_created

        self._mgr_user = tk.StringVar()
        self._mgr_pass = tk.StringVar()
        self._new_user = tk.StringVar()
        self._new_pass = tk.StringVar()
        self._role = tk.StringVar(value="employee")

        self._build_ui()

    def _build_ui(self) -> None:
        pad = {"padx": 10, "pady": 6}

        ttk.Label(self, text="Create Account", font=("Segoe UI", 16, "bold")).pack(
            pady=(20, 10)
        )

        form = ttk.Frame(self)
        form.pack(padx=32, pady=8)

        row = 0
        if self._require_manager_auth:
            ttk.Label(form, text="Manager authorization", font=("Segoe UI", 10, "bold")).grid(
                row=row, column=0, columnspan=2, sticky="w", pady=(0, 6)
            )
            row += 1
            ttk.Label(form, text="Manager username").grid(row=row, column=0, sticky="w", **pad)
            ttk.Entry(form, textvariable=self._mgr_user, width=32).grid(row=row, column=1, **pad)
            row += 1
            ttk.Label(form, text="Manager password").grid(row=row, column=0, sticky="w", **pad)
            ttk.Entry(form, textvariable=self._mgr_pass, width=32, show="•").grid(
                row=row, column=1, **pad
            )
            row += 1

        ttk.Label(form, text="New user", font=("Segoe UI", 10, "bold")).grid(
            row=row, column=0, columnspan=2, sticky="w", pady=(12, 6)
        )
        row += 1

        ttk.Label(form, text="Username").grid(row=row, column=0, sticky="w", **pad)
        ttk.Entry(form, textvariable=self._new_user, width=32).grid(row=row, column=1, **pad)
        row += 1

        ttk.Label(form, text="Password").grid(row=row, column=0, sticky="w", **pad)
        ttk.Entry(form, textvariable=self._new_pass, width=32, show="•").grid(row=row, column=1, **pad)
        row += 1

        ttk.Label(form, text="Role").grid(row=row, column=0, sticky="w", **pad)
        role_box = ttk.Combobox(
            form,
            textvariable=self._role,
            values=("employee", "manager", "owner"),
            state="readonly",
            width=30,
        )
        role_box.grid(row=row, column=1, **pad)
        row += 1

        self._error = ttk.Label(form, text="", foreground="#c0392b")
        self._error.grid(row=row, column=0, columnspan=2, sticky="w", padx=10, pady=6)

        btn_row = ttk.Frame(self)
        btn_row.pack(pady=16)
        ttk.Button(btn_row, text="Back", command=self._on_back).pack(side=tk.LEFT, padx=8)
        ttk.Button(btn_row, text="Create user", command=self._submit).pack(side=tk.LEFT, padx=8)

    def _submit(self) -> None:
        self._error.config(text="")

        new_u = self._new_user.get().strip()
        new_p = self._new_pass.get()
        role = self._role.get().strip()

        if not new_u or not new_p or not role:
            self._error.config(text="All fields are required.")
            return

        if self._require_manager_auth:
            mu = self._mgr_user.get().strip()
            mp = self._mgr_pass.get()
            if not mu or not mp:
                self._error.config(text="Manager username and password are required.")
                return
            if not verify_manager_credentials(mu, mp):
                self._error.config(text="Invalid manager credentials.")
                return
        else:
            user = self._app.current_user
            if not user or not db.is_manager_role(user["role"]):
                self._error.config(text="Only managers can create accounts.")
                messagebox.showerror("Access denied", "Only managers can create accounts.")
                return

        try:
            db.create_user(new_u, new_p, role)
        except sqlite3.IntegrityError:
            self._error.config(text="That username is already taken.")
            return
        except OSError as e:
            self._error.config(text=f"Database error: {e}")
            return

        messagebox.showinfo("Success", f"User '{new_u}' was created.")
        self._new_user.set("")
        self._new_pass.set("")
        self._mgr_user.set("")
        self._mgr_pass.set("")
        self._on_account_created()
