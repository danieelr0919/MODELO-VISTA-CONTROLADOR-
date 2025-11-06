from models.usuario_model import UsuarioModel

class UsuarioController:
    def __init__(self, view):
        self.view = view
        self.model = UsuarioModel()
    
    def guardar_usuario(self, username, email, password, imagen):
        success, message = self.model.crear_usuario(username, email, password)
        
        if success:
            self.view.mostrar_mensaje("Éxito", message)
            self.view.limpiar_campos()
            self.cargar_usuarios()
        else:
            self.view.mostrar_mensaje("Error", message, "error")
    
    def actualizar_usuario(self, user_id, username, email, password):
        success, message = self.model.actualizar_usuario(user_id, username, email, password)
        
        if success:
            self.view.mostrar_mensaje("Éxito", message)
            self.view.limpiar_campos()
            self.cargar_usuarios()
        else:
            self.view.mostrar_mensaje("Error", message, "error")
    
    def eliminar_usuario(self, user_id):
        success, message = self.model.eliminar_usuario(user_id)
        
        if success:
            self.view.mostrar_mensaje("Éxito", message)
            self.view.limpiar_campos()
            self.cargar_usuarios()
        else:
            self.view.mostrar_mensaje("Error", message, "error")
    
    def cargar_usuarios(self):
        usuarios = self.model.obtener_usuarios()
        self.view.actualizar_tabla(usuarios)