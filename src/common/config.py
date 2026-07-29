from pathlib import Path
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"

LANDING_DIR = DATA_DIR / "landing"
BRONZE_DIR = DATA_DIR / "bronze"
SILVER_DIR = DATA_DIR / "silver"
QUARENTINE_DIR = DATA_DIR / "quarentine"

POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
POSTGRES_DB_NAME = "logiflow_postgres"
POSTGRES_USER = "postgres"
POSTGRES_PASS = "postgres"
POSTGRES_CONFIG = {
    "url": f"jdbc:postgresql://{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}",
    "username": POSTGRES_USER,
    "password": POSTGRES_PASS,
    "host": POSTGRES_HOST,
    "port": POSTGRES_PORT,
    "db": POSTGRES_DB_NAME,
    
}

POSTGRES_CONFIG = SimpleNamespace(**POSTGRES_CONFIG)
