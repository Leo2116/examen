import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS retos (
            id SERIAL PRIMARY KEY,
            titulo VARCHAR(255) NOT NULL,
            descripcion TEXT,
            categoria VARCHAR(100),
            dificultad VARCHAR(10) CHECK (dificultad IN ('bajo', 'medio', 'alto')),
            estado VARCHAR(15) CHECK (estado IN ('pendiente', 'en proceso', 'completado'))
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
