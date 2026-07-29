import psycopg2
from psycopg2 import OperationalError

from src.common.config import POSTGRES_CONFIG

def get_connection():
    """
    Establishes and returns a connection to the PostgreSQL database.
    """
    try:
        connection = psycopg2.connect(
            host=POSTGRES_CONFIG.host,         
            port=POSTGRES_CONFIG.port,               
            database=POSTGRES_CONFIG.db,
            user=POSTGRES_CONFIG.username,           
            password=POSTGRES_CONFIG.password
        )
        return connection
        
    except OperationalError as error:
        print(f"Error: Unable to connect to the database.\nDetails: {error}")
        raise error
