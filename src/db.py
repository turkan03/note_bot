import sqlite3

# Function to establish a connection to the database
# Функция для установления соединения с базой данных
def get_connection():
  connection = sqlite3.connect("my_data.db")
  return connection

# Helper object that allows you to execute SQL commands and interact with the database
#Вспомогательный объект, позволяющий выполнять команды SQL и взаимодействовать с базой данных
cursor = connection.cursor()

