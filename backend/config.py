"""
Backward compatibility shim.
All functionality has been moved to backend.app.core.config
"""
from backend.app.core.config import Settings, get_settings

__all__ = ["Settings", "get_settings"]
