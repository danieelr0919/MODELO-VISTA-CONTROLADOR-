from .database import Database
from mysql.connector import Error

class ReporteModel:
    def __init__(self):
        self.db = Database()
    
    def generar_reporte_emocional(self, usuario_id):
        conn = self.db.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            query = """
            SELECT e.nombre, COUNT(ee.emocion_id) as frecuencia, MAX(en.fecha) as ultima_fecha
            FROM entrada_emocion ee 
            JOIN emociones e ON ee.emocion_id = e.id 
            JOIN entradas en ON ee.entrada_id = en.id 
            WHERE en.usuario_id = %s 
            GROUP BY e.nombre 
            ORDER BY frecuencia DESC
            """
            cursor.execute(query, (usuario_id,))
            return cursor.fetchall()
        except Error as e:
            print(f"Error al generar reporte: {e}")
            return []
        finally:
            if cursor:
                cursor.close()