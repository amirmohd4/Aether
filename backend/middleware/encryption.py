import base64
import hashlib
import os
import secrets

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class DataEncryptionService:
    """Authenticated encryption for sensitive application payloads.

    The key is supplied only by the server environment. There is deliberately
    no hard-coded production key or reversible base64-only "encryption".
    """

    KEY_ENV = "AETHER_ENCRYPTION_KEY"

    @classmethod
    def _key(cls) -> bytes:
        raw = os.getenv(cls.KEY_ENV, "")
        if not raw:
            raise RuntimeError(f"{cls.KEY_ENV} is required")
        try:
            key = base64.urlsafe_b64decode(raw.encode("ascii"))
        except Exception as exc:
            raise RuntimeError(f"{cls.KEY_ENV} must be URL-safe base64") from exc
        if len(key) not in {16, 24, 32}:
            raise RuntimeError(f"{cls.KEY_ENV} must decode to a 128, 192, or 256-bit key")
        return key

    @classmethod
    def encrypt_payload(cls, data: str) -> str:
        nonce = secrets.token_bytes(12)
        ciphertext = AESGCM(cls._key()).encrypt(nonce, data.encode("utf-8"), None)
        return base64.urlsafe_b64encode(nonce + ciphertext).decode("ascii")

    @classmethod
    def decrypt_payload(cls, token: str) -> str:
        try:
            raw = base64.urlsafe_b64decode(token.encode("ascii"))
            nonce, ciphertext = raw[:12], raw[12:]
            return AESGCM(cls._key()).decrypt(nonce, ciphertext, None).decode("utf-8")
        except Exception as exc:
            raise ValueError("Unable to decrypt payload") from exc

    @staticmethod
    def hash_national_id(id_string: str) -> str:
        return hashlib.sha256(id_string.strip().encode("utf-8")).hexdigest()
