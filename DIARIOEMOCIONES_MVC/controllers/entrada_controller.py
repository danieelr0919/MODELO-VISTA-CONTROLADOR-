from models.entrada_model import EntradaModel

class EntradaController:
    def __init__(self, view):
        self.view = view
        self.model = EntradaModel()
    
    def guardar_entrada(self, usuario_id, fecha, texto, emociones_ids):
        success, message = self.model.crear_entrada(usuario_id, fecha, texto, emociones_ids)
        
        if success:
            self.view.mostrar_mensaje("Éxito", message)
            self.view.limpiar_campos()
            self.cargar_entradas()
        else:
            self.view.mostrar_mensaje("Error", message, "error")
    
    def actualizar_entrada(self, entrada_id, usuario_id, fecha, texto):
        success, message = self.model.actualizar_entrada(entrada_id, usuario_id, fecha, texto)
        
        if success:
            self.view.mostrar_mensaje("Éxito", message)
            self.view.limpiar_campos()
            self.cargar_entradas()
        else:
            self.view.mostrar_mensaje("Error", message, "error")
    
    def eliminar_entrada(self, entrada_id):
        success, message = self.model.eliminar_entrada(entrada_id)
        
        if success:
            self.view.mostrar_mensaje("Éxito", message)
            self.view.limpiar_campos()
            self.cargar_entradas()
        else:
            self.view.mostrar_mensaje("Error", message, "error")
    
    def cargar_entradas(self):
        entradas = self.model.obtener_entradas()
        self.view.actualizar_tabla(entradas)