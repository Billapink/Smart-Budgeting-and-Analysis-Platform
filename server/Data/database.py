import sqlite3
from flask import g

DATABASE_FILE = 'budeting.sqlite'

def initTables():
    print('creating new database tables')
    g.db.executescript("""
    BEGIN;
    CREATE TABLE IF NOT EXISTS users(userID INTEGER PRIMARY KEY, username TEXT, password);
    CREATE UNIQUE INDEX IF NOT EXISTS username ON users (username);
    END;
    """)

def getDB():
    if "db" in g:
        return g.db
    
    g.db = sqlite3.connect(DATABASE_FILE)
    tables = g.db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'").fetchall()
    if (len(tables) == 0):
        initTables()
    return g.db