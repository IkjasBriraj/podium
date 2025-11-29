"""
Backward compatibility shim.
All functionality has been moved to backend.app.infrastructure.storage
"""
from backend.app.infrastructure.storage import Storage, storage

__all__ = ["Storage", "storage"]
