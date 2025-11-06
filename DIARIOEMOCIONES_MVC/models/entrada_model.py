from .database import Database
from mysql.connector import Error

class EntradaModel:
    def __init__(self):
        self.db = Database()
    
    def crear_entrada(self, usuario_id, fecha, texto, emociones_ids):
        conn = self.db.get_connection()
        if not conn:
            return False, "Error de conexión"
        
        try:
            cursor = conn.cursor()
            #
            cursor.callproc('sp_crear_entrada', (usuario_id, fecha, texto))
            
            # Obtener el ID de la entrada creada
            entrada_id = cursor.lastrowid
            
           
            if emociones_ids:
                emociones_lista = [eid.strip() for eid in emociones_ids.split(',')]
                for emocion_id in emociones_lista:
                    if emocion_id and emocion_id.isdigit():
                        query_relacion = "INSERT INTO entrada_emocion (entrada_id, emocion_id) VALUES (%s, %s)"
                        cursor.execute(query_relacion, (entrada_id, emocion_id))
            
            conn.commit()
            return True, "Entrada creada exitosamente"
        except Error as e:
            conn.rollback()
            return False, f"Error al crear entrada: {e}"
        finally:
            if cursor:
                cursor.close()
    
    def obtener_entradas(self):
        conn = self.db.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            
            cursor.callproc('sp_listar_entradas')
            
            entradas = []
            for result in cursor.stored_results():
                entradas = result.fetchall()
            
            return entradas
        except Error as e:
            print(f"Error al obtener entradas: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
    
    def actualizar_entrada(self, entrada_id, usuario_id, fecha, texto):
        conn = self.db.get_connection()
        if not conn:
            return False, "Error de conexión"
        
        try:
            cursor = conn.cursor()
            
            cursor.callproc('sp_actualizar_entrada', (entrada_id, usuario_id, fecha, texto))
            conn.commit()
            return True, f"Entrada {entrada_id} actualizada"
        except Error as e:
            conn.rollback()
            return False, f"Error al actualizar entrada: {e}"
        finally:
            if cursor:
                cursor.close()
    
    def eliminar_entrada(self, entrada_id):
        conn = self.db.get_connection()
        if not conn:
            return False, "Error de conexión"
        
        try:
            cursor = conn.cursor()
            
            cursor.callproc('sp_eliminar_entrada', (entrada_id,))
            conn.commit()
            return True, f"Entrada {entrada_id} eliminada"
        except Error as e:
            conn.rollback()
            return False, f"Error al eliminar entrada: {e}"
        finally:
            if cursor:
                cursor.close()