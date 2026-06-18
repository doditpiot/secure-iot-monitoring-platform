"""
Security helpers used by the device registry.

Author: HAMAILI Ahmed-Imad

This file intentionally keeps the security layer small. The current project is a
portfolio demo, but keys are still hashed before storage to model a safer design.
"""

import hashlib
import secrets


def hash_api_key(api_key: str) -> str:
    """Hash a device key before storing it in the database.

    The simulator sends the raw demo key, while PostgreSQL stores only the SHA256
    hash. This keeps the database model closer to a real device registry.
    """

    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()


def verify_api_key(raw_api_key: str, expected_hash: str) -> bool:
    """Compare a raw key with the stored hash using a timing-safe comparison."""

    candidate_hash = hash_api_key(raw_api_key)
    return secrets.compare_digest(candidate_hash, expected_hash)


def mask_api_key(api_key: str) -> str:
    """Return a display-safe version of a key for logs or API responses."""

    # Short keys are fully hidden because showing even a small part would reveal
    # too much information.
    if len(api_key) <= 8:
        return "****"

    return f"{api_key[:4]}...{api_key[-4:]}"
