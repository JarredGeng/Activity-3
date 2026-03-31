"""
Inactivity timeout: after a period without input, log the user out.

The monitor only runs while the user is logged in (started after successful login).
"""

from __future__ import annotations

import time
from typing import Callable, Optional

import tkinter as tk


class InactivityMonitor:
    """
    Tracks user activity on the Tk root window and calls on_timeout
    when no qualifying events occur for timeout_seconds.
    """

    def __init__(
        self,
        root: tk.Tk,
        timeout_seconds: float,
        on_timeout: Callable[[], None],
        poll_ms: int = 1000,
    ) -> None:
        self._root = root
        self._timeout_seconds = timeout_seconds
        self._on_timeout = on_timeout
        self._poll_ms = poll_ms
        self._last_activity = time.monotonic()
        self._after_id: Optional[str] = None
        self._bound = False

    def touch(self) -> None:
        """Reset the inactivity clock (call on successful login too)."""
        self._last_activity = time.monotonic()

    def start(self) -> None:
        """Bind global events and start the polling loop."""
        self.touch()
        if not self._bound:
            # Activity that should keep the session alive
            for seq in (
                "<Button-1>",
                "<Button-2>",
                "<Button-3>",
                "<KeyPress>",
                "<KeyRelease>",
                "<Motion>",
            ):
                self._root.bind_all(seq, self._on_activity, add="+")
            self._bound = True
        self._schedule_tick()

    def stop(self) -> None:
        """Cancel timers and unbind activity handlers."""
        if self._after_id is not None:
            try:
                self._root.after_cancel(self._after_id)
            except tk.TclError:
                pass
            self._after_id = None
        if self._bound:
            for seq in (
                "<Button-1>",
                "<Button-2>",
                "<Button-3>",
                "<KeyPress>",
                "<KeyRelease>",
                "<Motion>",
            ):
                try:
                    self._root.unbind_all(seq)
                except tk.TclError:
                    pass
            self._bound = False

    def _on_activity(self, event: tk.Event | None = None) -> None:
        self.touch()
        return None

    def _schedule_tick(self) -> None:
        self._after_id = self._root.after(self._poll_ms, self._tick)

    def _tick(self) -> None:
        elapsed = time.monotonic() - self._last_activity
        if elapsed >= self._timeout_seconds:
            self.stop()
            self._on_timeout()
            return
        self._schedule_tick()
