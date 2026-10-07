from __future__ import annotations

import os

from cryptography.fernet import Fernet, InvalidToken


_PREFIX = "fernet:v1:"


def _fernet() -> Fernet | None:
    raw = os.getenv("AETHER_ENCRYPTION_KEY", "").strip()
    if not raw:
        return None
    try:
        return Fernet(raw.encode("utf-8"))
    except Exception as exc:
        raise RuntimeError(
            "AETHER_ENCRYPTION_KEY must be a valid Fernet key "
            "(32-byte URL-safe base64)"
        ) from exc


def encrypt_text(value: str) -> str:
    if not value:
        return ""
    fernet = _fernet()
    if fernet is None:
        # Development keeps backwards-compatible plaintext behavior unless
        # encryption is explicitly configured. Production readiness requires it.
        return value
    return _PREFIX + fernet.encrypt(value.encode("utf-8")).decode("ascii")


def decrypt_text(value: str) -> str:
    if not value:
        return ""
    if not value.startswith(_PREFIX):
        return value

    fernet = _fernet()
    if fernet is None:
        raise RuntimeError(
            "AETHER_ENCRYPTION_KEY is required to decrypt protected document text"
        )
    try:
        token = value[len(_PREFIX):]
        return fernet.decrypt(token.encode("ascii")).decode("utf-8")
    except (InvalidToken, ValueError) as exc:
        raise RuntimeError("Encrypted document text could not be decrypted") from exc
