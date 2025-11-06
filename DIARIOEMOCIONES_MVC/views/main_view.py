import tkinter as tk
from tkinter import ttk
from .usuario_view import UsuarioView
from .emocion_view import EmocionView
from .entrada_view import EntradaView
from .reporte_view import ReporteView

class MainView:
    def __init__(self, root, controllers):
        self.root = root
        self.controllers = controllers
        self.configurar_ventana()
        self.configurar_estilo()
        self.crear_interfaz()
    
    def configurar_ventana(self):
        self.root.title("Diario de Emociones 🧠❤️")
        self.root.geometry("1000x800")
        self.root.configure(bg="#faf3e0")
        self.configurar_favicon()
    
    def configurar_favicon(self):
        try:
            self.root.iconbitmap("favicon.ico")
            print("✅ Favicon ICO cargado correctamente")
        except Exception as e:
            print(f"❌ Error cargando favicon ICO: {e}")
    
    def configurar_estilo(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background="#faf3e0")
        style.configure("TNotebook.Tab",
                        background="#e0d3c1",
                        foreground="#5a4a42",
                        font=("Arial", 11, "bold"),
                        padding=[12, 6])
        style.map("TNotebook.Tab",
                  background=[("selected", "#d4a5a5")],
                  foreground=[("selected", "white")])

        # Estilo para Treeview (tablas)
        style.configure("Treeview",
                        background="#ffffff",
                        foreground="#5a4a42",
                        rowheight=25,
                        fieldbackground="#ffffff")
        style.configure("Treeview.Heading",
                        background="#d4a5a5",
                        foreground="white",
                        font=("Arial", 10, "bold"))
        style.map("Treeview",
                  background=[('selected', '#e77f67')])
    
    def crear_interfaz(self):
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Crear pestañas
        self.crear_pestanas()
        
        # Footer
        self.crear_footer()
    
    def crear_pestanas(self):
        # Pestaña Usuarios
        self.tab_usuarios = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_usuarios, text=" 👤 Usuarios ")
        self.usuario_view = UsuarioView(self.tab_usuarios, self.controllers['usuario'])
        
        # Pestaña Emociones
        self.tab_emociones = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_emociones, text=" 😊 Emociones ")
        self.emocion_view = EmocionView(self.tab_emociones, self.controllers['emocion'])
        
        # Pestaña Entradas
        self.tab_entradas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_entradas, text=" 📖 Entradas ")
        self.entrada_view = EntradaView(self.tab_entradas, self.controllers['entrada'])
        
        # Pestaña Reportes
        self.tab_reportes = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_reportes, text=" 📈 Reportes ")
        self.reporte_view = ReporteView(self.tab_reportes, self.controllers['reporte'])
    
    def crear_footer(self):
        footer = tk.Label(self.root, text="Diario de Emociones v1.0 — Tu espacio seguro para sentir 🌿",
                          font=("Arial", 10, "italic"), fg="#7d6e65", bg="#faf3e0")
        footer.pack(side=tk.BOTTOM, pady=15)