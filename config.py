import os

class Config:
    DB_HOST = os.getenv("DB_HOST", "localhost")  # Default to localhost
    DB_NAME = os.getenv("DB_NAME", "Zones")      # Default database name
    DB_USER = os.getenv("DB_USER", "postgres")   # Default user
    DB_PASS = os.getenv("DB_PASS", "dost")       # Default password
