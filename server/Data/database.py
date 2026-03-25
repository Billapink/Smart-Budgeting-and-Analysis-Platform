import sqlite3
from flask import g

DATABASE_FILE = 'budeting.sqlite'

def initTables():
    print('creating new database tables')
    g.db.executescript("""
    BEGIN;
    CREATE TABLE IF NOT EXISTS users(userID INTEGER PRIMARY KEY, username, password);
    CREATE UNIQUE INDEX IF NOT EXISTS username ON users (username);
                       
    CREATE TABLE IF NOT EXISTS companies(companyID INTEGER PRIMARY KEY, company_name, company_code INTEGER);
    CREATE TABLE IF NOT EXISTS memberships(
        membershipID INTEGER PRIMARY KEY, 
        userID INTEGER,
        companyID INTEGER,
        role,
        FOREIGN KEY(userID) REFERENCES users(userID),
        FOREIGN KEY(companyID) REFERENCES companies(companyID)
    );
    CREATE TABLE IF NOT EXISTS categories(
        categoryID INTEGER PRIMARY KEY, 
        companyID INTEGER,
        category_name,
        type,
        FOREIGN KEY(companyID) REFERENCES companies(companyID)
    );
    CREATE TABLE IF NOT EXISTS category_rules(
        ruleID INTEGER PRIMARY KEY, 
        categoryID INTEGER, 
        companyID INTEGER,
        match_type,
        pattern,
        priority INTEGER,
        active INTEGER,
        FOREIGN KEY(categoryID) REFERENCES categories(categoryID),
        FOREIGN KEY(companyID) REFERENCES companies(companyID)
    );
    CREATE TABLE IF NOT EXISTS transactions(
        transactionID INTEGER PRIMARY KEY, 
        categoryID INTEGER,
        companyID INTEGER, 
        date, 
        amount,
        merchant,
        direction,
        FOREIGN KEY(categoryID) REFERENCES categories(categoryID),
        FOREIGN KEY(companyID) REFERENCES companies(companyID)
    );
    CREATE TABLE IF NOT EXISTS budgets(
        budgetID INTEGER PRIMARY KEY, 
        categoryID INTEGER,
        created_by INTEGER, 
        date, 
        budget,
        FOREIGN KEY(categoryID) REFERENCES categories(categoryID),
        FOREIGN KEY(created_by) REFERENCES users(userID)
    );
    END;
    """)

def getDB():
    if "db" in g:
        return g.db
    
    g.db = sqlite3.connect(DATABASE_FILE)
    tables = g.db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'").fetchall()
    print('NUMBER OF TABLES', len(tables))
    if (len(tables) < 5):
        initTables()
    return g.db