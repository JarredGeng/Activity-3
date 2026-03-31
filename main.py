"""
Store GUI — entry point.

Shows login first, then routes by role (employee vs manager/owner).
Starts inactivity monitoring after a successful login.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from db import init_db
from session import InactivityMonitor
from ui.create_account import CreateAccountScreen
from ui.employee_dashboard import EmployeeDashboard
from ui.login_screen import LoginScreen
from ui.manager_dashboard import ManagerDashboard

# Inactivity window (seconds). Requirement: roughly 30–60 seconds.
SESSION_TIMEOUT_SECONDS = 45.0


class StoreApp:
    """Owns the root window, navigation between screens, and session timeout."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Store Management")
        self.root.geometry("1280x800")
        self.root.minsize(800, 500)

        self.current_user: dict | None = None
        self._container = ttk.Frame(self.root)
        self._container.pack(fill=tk.BOTH, expand=True)

        self._session: InactivityMonitor | None = None

        init_db()
        self.show_login()

    def run(self) -> None:
        self.root.mainloop()

    # --- navigation ---------------------------------------------------------

    def show_login(self) -> None:
        """Return to login and clear session state."""
        self._stop_session()
        self.current_user = None
        self._clear_container()
        screen = LoginScreen(
            self._container,
            self,
            on_login_success=self._on_login_success,
            on_open_create_account=self._open_create_account_from_login,
        )
        screen.pack(fill=tk.BOTH, expand=True)

    def _on_login_success(self, user: dict) -> None:
        """Route to the correct dashboard and start inactivity monitoring."""
        self.current_user = user
        self._start_session()
        role = user.get("role")
        if role == "employee":
            self.show_employee_dashboard()
        else:
            # manager and owner use the same dashboard (create account, etc.)
            self.show_manager_dashboard()

    def show_employee_dashboard(self) -> None:
        self._clear_container()
        self._touch_session()
        screen = EmployeeDashboard(
            self._container,
            self,
            on_logout=self.show_login,
        )
        screen.pack(fill=tk.BOTH, expand=True)

    def show_manager_dashboard(self) -> None:
        self._clear_container()
        self._touch_session()
        screen = ManagerDashboard(
            self._container,
            self,
            on_logout=self.show_login,
            on_create_account=self._open_create_account_from_manager,
        )
        screen.pack(fill=tk.BOTH, expand=True)

    def _open_create_account_from_login(self) -> None:
        """Login screen: creating users still requires manager credentials on the form."""
        self._stop_session()
        self.current_user = None
        self._clear_container()
        screen = CreateAccountScreen(
            self._container,
            self,
            require_manager_auth=True,
            on_back=self.show_login,
            on_account_created=self.show_login,
        )
        screen.pack(fill=tk.BOTH, expand=True)

    def _open_create_account_from_manager(self) -> None:
        """Logged-in manager: no extra manager fields; role is checked on submit."""
        self._clear_container()
        self._touch_session()
        screen = CreateAccountScreen(
            self._container,
            self,
            require_manager_auth=False,
            on_back=self.show_manager_dashboard,
            on_account_created=self.show_manager_dashboard,
        )
        screen.pack(fill=tk.BOTH, expand=True)

    def _clear_container(self) -> None:
        for child in self._container.winfo_children():
            child.destroy()

    # --- session / timeout --------------------------------------------------

    def _start_session(self) -> None:
        self._stop_session()
        self._session = InactivityMonitor(
            self.root,
            SESSION_TIMEOUT_SECONDS,
            self._on_inactivity_timeout,
        )
        self._session.start()

    def _touch_session(self) -> None:
        if self._session is not None:
            self._session.touch()

    def _stop_session(self) -> None:
        if self._session is not None:
            self._session.stop()
            self._session = None

    def _on_inactivity_timeout(self) -> None:
        """Log out and show login again."""
        self.current_user = None
        try:
            messagebox.showinfo(
                "Session expired",
                "You were logged out due to inactivity.",
            )
        except tk.TclError:
            pass
        self.show_login()


def main() -> None:
    app = StoreApp()
    app.run()


if __name__ == "__main__":
    main()
