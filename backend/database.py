"""
Backward compatibility shim.
All functionality has been moved to backend.app.db.mongodb
"""
from backend.app.db.mongodb import Database, db, get_database

__all__ = ["Database", "db", "get_database"]
