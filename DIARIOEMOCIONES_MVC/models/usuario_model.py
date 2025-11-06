from .database import Database
from mysql.connector import Error
import hashlib

class UsuarioModel:
    def __init__(self):
        self.db = Database()
    
    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def crear_usuario(self, username, email, password):
        conn = self.db.get_connection()
        if not conn:
            return False, "Error de conexión a la base de datos"
        
        try:
            cursor = conn.cursor()
            hashed_password = self._hash_password(password)
            cursor.callproc('sp_crear_usuario', (username, email, hashed_password))
            conn.commit()
            return True, f"Usuario {username} creado exitosamente"
        except Error as e:
            conn.rollback()
            return False, f"Error al crear usuario: {e}"
        finally:
            if cursor:
                cursor.close()
    
    def obtener_usuarios(self):
        conn = self.db.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.callproc('sp_listar_usuarios')
            for result in cursor.stored_results():
                return result.fetchall()
            return []
        except Error as e:
            print(f"Error al obtener usuarios: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
    
    def actualizar_usuario(self, user_id, username, email, password=None):
        conn = self.db.get_connection()
        if not conn:
            return False, "Error de conexión"
        
        try:
            cursor = conn.cursor()
            
            if password:
                hashed_password = self._hash_password(password)
                
                cursor.callproc('sp_actualizar_usuario', (user_id, username, email, hashed_password))
            else:
                # Obtener password actual y usar SP
                cursor.execute("SELECT password_hash FROM usuarios WHERE id = %s", (user_id,))
                current_password = cursor.fetchone()[0]
                
                cursor.callproc('sp_actualizar_usuario', (user_id, username, email, current_password))
            
            conn.commit()
            return True, f"Usuario {user_id} actualizado exitosamente"
        except Error as e:
            conn.rollback()
            return False, f"Error al actualizar usuario: {e}"
        finally:
            if cursor:
                cursor.close()
    
    def eliminar_usuario(self, user_id):
        conn = self.db.get_connection()
        if not conn:
            return False, "Error de conexión"
        
        try:
            cursor = conn.cursor()
            
            cursor.callproc('sp_eliminar_usuario', (user_id,))
            conn.commit()
            return True, f"Usuario {user_id} eliminado exitosamente"
        except Error as e:
            conn.rollback()
            return False, f"Error al eliminar usuario: {e}"
        finally:
            if cursor:
                cursor.close()