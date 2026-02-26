"""Backward-compatible facade for dependency functions.

The real implementations live in ``api.deps``; this module simply
re-exports them so existing imports keep working.
"""

from api.deps import api_key_auth, get_db  # noqa: F401

