"""
Tests for device key helpers.

Author: HAMAILI Ahmed-Imad
"""

from app.core.security import hash_api_key, verify_api_key


def test_api_key_hash_is_stable():
    """The same raw key should always produce the same hash."""

    assert hash_api_key("demo-key") == hash_api_key("demo-key")


def test_api_key_verification_accepts_valid_key():
    """A matching raw key should validate against its stored hash."""

    stored_hash = hash_api_key("demo-key")
    assert verify_api_key("demo-key", stored_hash) is True


def test_api_key_verification_rejects_invalid_key():
    """A wrong raw key should never validate against another key hash."""

    stored_hash = hash_api_key("demo-key")
    assert verify_api_key("wrong-key", stored_hash) is False
