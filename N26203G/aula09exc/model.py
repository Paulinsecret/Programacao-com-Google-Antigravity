import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "clinica.db")

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def init_db():
    """Initializes the database and creates the pets table if it does not exist."""
    query = """
    CREATE TABLE IF NOT EXISTS pets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        species TEXT NOT NULL,
        name TEXT NOT NULL,
        breed TEXT NOT NULL,
        age TEXT NOT NULL,
        owner TEXT NOT NULL,
        severity TEXT NOT NULL,
        is_hospitalized BOOLEAN NOT NULL
    );
    """
    conn = get_db_connection()
    try:
        conn.execute(query)
        conn.commit()
    finally:
        conn.close()

def add_pet(species, name, breed, age, owner, severity, is_hospitalized):
    """Inserts a new pet registration into the database."""
    query = """
    INSERT INTO pets (species, name, breed, age, owner, severity, is_hospitalized)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, (species, name, breed, age, owner, severity, 1 if is_hospitalized else 0))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def get_all_pets():
    """Retrieves all registered pets from the database."""
    query = "SELECT * FROM pets ORDER BY id DESC;"
    conn = get_db_connection()
    try:
        rows = conn.execute(query).fetchall()
        # Convert sqlite3.Row objects to dictionaries
        result = []
        for row in rows:
            d = dict(row)
            # convert SQLite integer 0/1 back to JSON boolean True/False
            d['is_hospitalized'] = bool(d['is_hospitalized'])
            result.append(d)
        return result
    finally:
        conn.close()
