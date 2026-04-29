import sqlite3
import os

DB_PATH = "database.db"

def init_db():
    # Cria o arquivo do banco se não existir
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Cria a tabela de casos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS log_cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        error_hash TEXT,
        summary TEXT,
        cause TEXT,
        solution TEXT
    )
    """)
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Para retornar resultados como dicionários
    return conn
