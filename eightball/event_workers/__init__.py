"""Explicit event workers. Importing this package never starts processing."""

from .service import EventWorkerService

__all__ = ['EventWorkerService']
