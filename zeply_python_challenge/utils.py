import hashlib

from zeply_python_challenge.config import settings


def make_hash(*, value: str) -> str:
    """Return hashed value of the given string."""
    return hashlib.md5(f"{settings.HASH_SALT}{value}".encode()).hexdigest()
