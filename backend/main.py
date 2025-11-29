"""
Backward compatibility shim for existing uvicorn command.
All functionality has been moved to backend.app.main
"""
from backend.app.main import app

__all__ = ["app"]
