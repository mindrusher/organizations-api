"""Backward-compatible database module.

For production use, the real configuration lives in ``db.session``.
This module re-exports the same symbols to avoid breaking imports.
"""

from db.session import Base, SessionLocal, engine  # noqa: F401
