# src/db.py - Base de datos SQLite 13 tablas
import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "../data/skandia.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS series (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idp TEXT NOT NULL,
        period TEXT NOT NULL,
        series TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS metricas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idp TEXT NOT NULL,
        rent365 REAL,
        rent30 REAL,
        sharpe REAL,
        volatilidad REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS alertas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idp TEXT,
        tipo TEXT,
        mensaje TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS portafolio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        idp TEXT,
        monto REAL,
        fecha_entrada DATE,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    conn.close()
    print("DB inicializada OK")

def save_data(idp, series, period="P4"):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO series (idp, period, series) VALUES (?, ?, ?)",
        (idp, period, json.dumps(series))
    )
    conn.commit()
    conn.close()

def save_metricas(idp, rent365, rent30, sharpe, vol):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO metricas (idp, rent365, rent30, sharpe, volatilidad) VALUES (?, ?, ?, ?, ?)",
        (idp, rent365, rent30, sharpe, vol)
    )
    conn.commit()
    conn.close()

def save_alerta(idp, tipo, mensaje):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO alertas (idp, tipo, mensaje) VALUES (?, ?, ?)",
        (idp, tipo, mensaje)
    )
    conn.commit()
    conn.close()

def get_last_metricas():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT idp, rent365, rent30, sharpe, volatilidad, timestamp
        FROM metricas
        WHERE timestamp = (SELECT MAX(timestamp) FROM metricas m2 WHERE m2.idp = metricas.idp)
    """)
    rows = c.fetchall()
    conn.close()
    return {r[0]: {"rent365": r[1], "rent30": r[2], "sharpe": r[3], "vol": r[4], "ts": r[5]} for r in rows}
