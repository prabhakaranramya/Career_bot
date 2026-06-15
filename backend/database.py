import sqlite3
import json
from datetime import datetime
import os

# Get the directory where this file is
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "conversations.db")

print(f"Database path: {DB_PATH}")  # Debug line

def init_db():
    """Create database tables if they don't exist"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS conversations
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id TEXT NOT NULL,
                      title TEXT DEFAULT "New Chat",
                      messages TEXT NOT NULL,
                      created_at TEXT,
                      updated_at TEXT)''')
        
        conn.commit()
        conn.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")

def save_conversation(user_id: str, title: str, messages: list):
    """Save or update a conversation"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        c.execute('SELECT id FROM conversations WHERE user_id = ? AND title = ?', (user_id, title))
        exists = c.fetchone()
        
        if exists:
            c.execute('''UPDATE conversations 
                         SET messages = ?, updated_at = ?
                         WHERE user_id = ? AND title = ?''',
                      (json.dumps(messages), datetime.now().isoformat(), user_id, title))
        else:
            c.execute('''INSERT INTO conversations 
                         (user_id, title, messages, created_at, updated_at)
                         VALUES (?, ?, ?, ?, ?)''',
                      (user_id, title, json.dumps(messages), 
                       datetime.now().isoformat(), datetime.now().isoformat()))
        
        conn.commit()
    finally:
        conn.close()

def load_conversation(user_id: str, title: str = "New Chat"):
    """Load a conversation"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        c.execute('''SELECT messages FROM conversations 
                     WHERE user_id = ? AND title = ?''', (user_id, title))
        result = c.fetchone()
        return json.loads(result[0]) if result else []
    finally:
        conn.close()

def list_conversations(user_id: str):
    """List all conversations for a user"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        c.execute('''SELECT title, updated_at FROM conversations 
                     WHERE user_id = ?
                     ORDER BY updated_at DESC''', (user_id,))
        results = c.fetchall()
        return [{"title": r[0], "updated_at": r[1]} for r in results]
    finally:
        conn.close()

def delete_conversation(user_id: str, title: str):
    """Delete a conversation"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        c.execute('''DELETE FROM conversations 
                     WHERE user_id = ? AND title = ?''', (user_id, title))
        conn.commit()
    finally:
        conn.close()

# Initialize database when module is imported
init_db()