import sqlite3

# Function to establish a connection to the database
# Функция для установления соединения с базой данных
def get_connection():
  connection = sqlite3.connect("my_data.db")
  return connection

