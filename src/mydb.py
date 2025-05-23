import sqlite3

try:
  with sqlite3.connect("my_data.db") as conn:
    print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")
    cursor = conn.cursor()
    # Creat tables for database
    cursor.execute('''
      CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        user INTEGER NOT NULL UNIQUE
      );
    ''')
    cursor.execute('''
      CREATE TABLE IF NOT EXISTS notes(
        note_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        note_title TEXT NOT NULL,
        note_content TEXT NOT NULL,
        category_name TEXT,
        FOREIGN KEY (user_id) REFERENCES user(user_id) 
      );
    ''')
    conn.commit() 
except sqlite3.OperationalError as e:
  print("Failed to open database:", e)


 # Add data in tables
def user_value(value):
   with sqlite3.connect("my_data.db") as conn:
    cursor = conn.cursor()
    cursor.execute('''
            INSERT OR IGNORE INTO users(user)
            VALUES (?)
           ''', (value,))
    conn.commit()
        
def notes(title,content, category, user_id):
   with sqlite3.connect("my_data.db") as conn:
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO notes(note_title,note_content,category_name, user_id) 
        VALUES (?,?,?,?)''', (title, content, category, user_id,))
    conn.commit()


# Sekect distinct categories for user

def categories(user_id):
  with sqlite3.connect("my_data.db") as conn:
    cursor = conn.cursor()
    cursor.execute('''
       SELECT DISTINCT category_name FROM notes WHERE user_id = ?''', (user_id,))
    rows = cursor.fetchall()
    return rows
  conn.commit()
