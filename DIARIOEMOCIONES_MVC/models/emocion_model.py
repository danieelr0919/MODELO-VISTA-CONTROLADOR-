from .database import Database
from mysql.connector import Error

class EmocionModel:
    def __init__(self):
        self.db = Database()
    
    def crear_emocion(self, nombre):
        conn = self.db.get_connection()
        if not conn:
            return False, "Error de conexión"
        
        try:
            cursor = conn.cursor()
            cursor.callproc('sp_crear_emocion', (nombre,))
            conn.commit()
            return True, f"Emoción {nombre} creada exitosamente"
        except Error as e:
            conn.rollback()
            return False, f"Error al crear emoción: {e}"
        finally:
            if cursor:
                cursor.close()
    
    def obtener_emociones(self):
        conn = self.db.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.callproc('sp_listar_emociones')
            
            emociones = []
            for result in cursor.stored_results():
                emociones = result.fetchall()
            
            return emociones
        except Error as e:
            print(f"Error al obtener emociones: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
    
    def actualizar_emocion(self, emocion_id, nombre):
        conn = self.db.get_connection()
        if not conn:
            return False, "Error de conexión"
        
        try:
            cursor = conn.cursor()
            
            cursor.callproc('sp_actualizar_emocion', (emocion_id, nombre))
            conn.commit()
            return True, f"Emoción {emocion_id} actualizada"
        except Error as e:
            conn.rollback()
            return False, f"Error al actualizar emoción: {e}"
        finally:
            if cursor:
                cursor.close()
    
    def eliminar_emocion(self, emocion_id):
        conn = self.db.get_connection()
        if not conn:
            return False, "Error de conexión"
        
        try:
            cursor = conn.cursor()
        
            cursor.callproc('sp_eliminar_emocion', (emocion_id,))
            conn.commit()
            return True, f"Emoción {emocion_id} eliminada"
        except Error as e:
            conn.rollback()
            return False, f"Error al eliminar emoción: {e}"
        finally:
            if cursor:
                cursor.close()