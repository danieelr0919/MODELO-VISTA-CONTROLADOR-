import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='diario_emociones',
                user='root',
                password=''
            )
            if self.connection.is_connected():
                print("✅ Conexión a base de datos exitosa")
        except Error as e:
            print(f"❌ Error de conexión: {e}")
            self.connection = None
    
    def get_connection(self):
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        return self.connection
    
    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("❌ Conexión a base de datos cerrada")