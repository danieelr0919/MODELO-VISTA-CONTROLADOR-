from models.emocion_model import EmocionModel

class EmocionController:
    def __init__(self, view):
        self.view = view
        self.model = EmocionModel()
    
    def guardar_emocion(self, nombre, imagen):
        success, message = self.model.crear_emocion(nombre)
        
        if success:
            self.view.mostrar_mensaje("Éxito", message)
            self.view.limpiar_campos()
            self.cargar_emociones()
        else:
            self.view.mostrar_mensaje("Error", message, "error")
    
    def actualizar_emocion(self, emocion_id, nombre):
        success, message = self.model.actualizar_emocion(emocion_id, nombre)
        
        if success:
            self.view.mostrar_mensaje("Éxito", message)
            self.view.limpiar_campos()
            self.cargar_emociones()
        else:
            self.view.mostrar_mensaje("Error", message, "error")
    
    def eliminar_emocion(self, emocion_id):
        success, message = self.model.eliminar_emocion(emocion_id)
        
        if success:
            self.view.mostrar_mensaje("Éxito", message)
            self.view.limpiar_campos()
            self.cargar_emociones()
        else:
            self.view.mostrar_mensaje("Error", message, "error")
    
    def cargar_emociones(self):
        emociones = self.model.obtener_emociones()
        self.view.actualizar_tabla(emociones)