import sqlite3

try:
  with sqlite3.connect("my_data.db") as conn:
    print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")
    cursor = conn.cursor()

    cursor.execute('''
      CREATE TABLE IF NOT EXISTS user(
        user_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL
      );
    ''')

    cursor.execute('''
      CREATE TABLE IF NOT EXISTS categories(
        category_id INTEGER PRIMARY KEY,
        category_name TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES user(user_id) 
      );
    ''')

    cursor.execute('''
      CREATE TABLE IF NOT EXISTS notes(
      note_id INTEGER PRIMARY KEY,
      note_title TEXT NOT NULL,
      note_content TEXT,
      user_id INTEGER NOT NULL,
      category_id INTEGER,
      FOREIGN KEY (user_id) REFERENCE user(user_id),
      FOREIGN KEY (category_id) REFERENCE categories(category_id)
      );
    ''')
    
    conn.commit()
except sqlite3.OperationalError as e:
  print("Failed to open database:", e)





