"""Event publisher stubs for permission changes."""

from dataclasses import dataclass
from datetime import datetime
from typing import Callable


@dataclass
class PermissionEvent:
    user_id: int
    role_level: int
    timestamp: datetime


def publish_permission_granted(event: PermissionEvent, sink: Callable[[PermissionEvent], None] | None = None) -> None:
    """Publish a permission granted event. Defaults to logging via print."""

    sink = sink or (lambda evt: print(f"[permission_granted] {evt}"))  # pragma: no cover - logging helper
    sink(event)