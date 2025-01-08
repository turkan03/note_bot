import sqlite3

# Function to establish a connection to the database
# Функция для установления соединения с базой данных
def get_connection():
  connection = sqlite3.connect("my_data.db")
  return connection

# Helper object that allows you to execute SQL commands and interact with the database
#Вспомогательный объект, позволяющий выполнять команды SQL и взаимодействовать с базой данных
cursor = connection.cursor()

# Create table with user nickname or names 
CREAT TABLE IF NOT EXIST users(
  user_id INTEGER PRIMARY KEY,
  usename TEXT NOT NULL
)

# Create table with user categories and connect it with user name
CREAT TABLE IF NOT EXIST categories(
  category_id INTEGER PRIMARY KEY,
  category_name TEXT NOT NULL,
  user_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(user_id)

)

# Creat table for notes 
CREAT TABLE IF NOT EXIST notes(
  note_id INTEGER PRIMARY KEY,
  note_title TEXT NOT NULL,
  note_content TEXT,
  user_id INTEGER NOT NULL,
  category_id INTEGER,
  FOREIGN KEY (user_id) REFERENCE users(user_id),
  FOREIGN KEY (category_id) REFERENCE categories(category_id)

)