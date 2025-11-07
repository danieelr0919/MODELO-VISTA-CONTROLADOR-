import tkinter as tk
from views.main_view import MainView
from controllers.usuario_controller import UsuarioController
from controllers.emocion_controller import EmocionController
from controllers.entrada_controller import EntradaController
from controllers.reportes_controller import ReporteController

class DiarioEmocionesApp:
    def __init__(self):
        self.root = tk.Tk()
        
        try:
            self.root.iconbitmap("favicon.ico")
            print("✅ Favicon ICO cargado correctamente")
        except Exception as e:
            print(f"❌ Error al cargar el favicon: {e}")
        
        self.controllers = {}
        self.inicializar_controladores()
        self.view = MainView(self.root, self.controllers)
        self.conectar_vistas_con_controladores()
        self.cargar_datos_iniciales()

    def inicializar_controladores(self):
        # Crear controladores (las vistas se conectarán después)
        self.controllers['usuario'] = UsuarioController(None)
        self.controllers['emocion'] = EmocionController(None)
        self.controllers['entrada'] = EntradaController(None)
        self.controllers['reporte'] = ReporteController(None)

    def conectar_vistas_con_controladores(self):
        # Conectar cada controlador con su vista
        self.controllers['usuario'].view = self.view.usuario_view
        self.controllers['emocion'].view = self.view.emocion_view
        self.controllers['entrada'].view = self.view.entrada_view
        self.controllers['reporte'].view = self.view.reporte_view

    def cargar_datos_iniciales(self):
        # Cargar datos iniciales en las tablas
        self.controllers['usuario'].cargar_usuarios()
        self.controllers['emocion'].cargar_emociones()
        self.controllers['entrada'].cargar_entradas()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DiarioEmocionesApp()
    app.run()