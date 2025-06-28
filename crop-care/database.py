import sqlite3
from sqlite3 import Error
from werkzeug.security import generate_password_hash, check_password_hash

def create_connection():
    """
    Create a database connection to the SQLite database specified by the file.
    Returns a connection object with row_factory set to sqlite3.Row for dict-like access.
    """
    try:
        conn = sqlite3.connect('cropcare.db')
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_user(conn, username, email, password):
    """
    Create a new user in the users table with hashed password.
    Returns the new user's id on success, None on failure.
    """
    try:
        hashed_pw = generate_password_hash(password)
        conn.execute(
            'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
            (username, email, hashed_pw)
        )
        conn.commit()
        # Get the last inserted row id
        user_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        return user_id
    except Error as e:
        print(f"Error creating user: {e}")
        return None

def verify_user(conn, username, password):
    """
    Verify user credentials.
    Returns the user row if credentials are correct, else None.
    """
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    if user and check_password_hash(user['password'], password):
        return user
    return None

def init_db():
    """
    Initialize the database and create tables if they don't exist.
    """
    conn = create_connection()
    if conn is None:
        print("Failed to create database connection. Cannot initialize DB.")
        return
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
