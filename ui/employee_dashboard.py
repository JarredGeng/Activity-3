"""
Employee dashboard: limited view; no account creation.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from main import StoreApp


class EmployeeDashboard(ttk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        app: "StoreApp",
        *,
        on_logout: Callable[[], None],
    ) -> None:
        super().__init__(parent)
        self._app = app
        self._on_logout = on_logout
        self._build_ui()

    def _build_ui(self) -> None:
        header = ttk.Frame(self)
        header.pack(fill=tk.X, padx=16, pady=12)
        ttk.Label(header, text="Employee Dashboard", font=("Segoe UI", 18, "bold")).pack(
            side=tk.LEFT
        )
        ttk.Button(header, text="Log out", command=self._on_logout).pack(side=tk.RIGHT)

        body = ttk.Frame(self)
        body.pack(fill=tk.BOTH, expand=True, padx=24, pady=16)
        ttk.Label(
            body,
            text=(
                "Welcome. This is the employee view.\n"
                "Account creation and management tools are not available here."
            ),
            justify=tk.LEFT,
        ).pack(anchor="w")
