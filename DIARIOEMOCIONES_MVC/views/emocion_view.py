import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image

class EmocionView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Título
        titulo = tk.Label(self.parent, text="😊 Catálogo de Emociones", font=("Arial", 16, "bold"), fg="#b86d6d",
                          bg="#faf3e0")
        titulo.pack(pady=(20, 10))

        # Frame del formulario
        form_frame = tk.Frame(self.parent, bg="#f8f0e3", padx=20, pady=20, relief="groove", bd=1)
        form_frame.pack(pady=10, padx=20, fill="x")

        # Campos del formulario
        tk.Label(form_frame, text="ID Emoción:", bg="#f8f0e3", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        self.emocion_id_entry = tk.Entry(form_frame, width=30)
        self.emocion_id_entry.grid(row=0, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Nombre:", bg="#f8f0e3", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.nombre_emocion_entry = tk.Entry(form_frame, width=30)
        self.nombre_emocion_entry.grid(row=1, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Imagen de la Emoción:", bg="#f8f0e3", font=("Arial", 12)).grid(row=2, column=0, sticky="w")
        self.imagen_emocion_path = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.imagen_emocion_path, width=30).grid(row=2, column=1, sticky="w", pady=5)
        tk.Button(form_frame, text="Seleccionar Imagen", command=self.seleccionar_imagen_emocion).grid(row=3, column=1, sticky="w", padx=5, pady=5)

        # Botones
        btn_frame = tk.Frame(self.parent, bg="#faf3e0")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="💾 Guardar", bg="#88c9a1", fg="white", width=12,
                  command=self.guardar_emocion).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✏️ Actualizar", bg="#a2b9bc", fg="white", width=12,
                  command=self.actualizar_emocion).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑️ Eliminar", bg="#e77f67", fg="white", width=12,
                  command=self.eliminar_emocion).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🧹 Limpiar", bg="#f5c091", fg="#5a4a42", width=12,
                  command=self.limpiar_campos).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🔄 Cargar Datos", bg="#a2b9bc", fg="white", width=12,
                  command=self.cargar_emociones).pack(side=tk.LEFT, padx=5)
        
        # En la sección de botones, agregar:
        tk.Button(btn_frame, text="📊 Exportar Excel", bg="#4a90e2", fg="white", width=15,
                  command=self.exportar_excel).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="📄 Exportar PDF", bg="#ED7D31", fg="white", width=15,
                  command=self.exportar_pdf).pack(side=tk.LEFT, padx=5)

def exportar_excel(self):
    try:
        from exportadores.exportador_central import ExportadorCentral
        exportador = ExportadorCentral()
        
        emociones = []
        for item in self.tabla_emociones.get_children():
            emociones.append(self.tabla_emociones.item(item)['values'])
        
        if emociones:
            exportador.exportar_excel("emociones", emociones)
        else:
            self.mostrar_mensaje("Advertencia", "No hay emociones para exportar", "warning")
            
    except Exception as e:
        self.mostrar_mensaje("Error", f"No se pudo exportar: {e}", "error")

def exportar_pdf(self):
    try:
        from exportadores.exportador_central import ExportadorCentral
        exportador = ExportadorCentral()
        
        emociones = []
        for item in self.tabla_emociones.get_children():
            emociones.append(self.tabla_emociones.item(item)['values'])
        
        if emociones:
            exportador.exportar_pdf("emociones", emociones)
        else:
            self.mostrar_mensaje("Advertencia", "No hay emociones para exportar", "warning")
            
    except Exception as e:
        self.mostrar_mensaje("Error", f"No se pudo exportar: {e}", "error")

        # TABLA DE EMOCIONES
        tabla_frame = tk.Frame(self.parent, bg="#faf3e0")
        tabla_frame.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Label(tabla_frame, text="📋 Catálogo de Emociones", font=("Arial", 14, "bold"),
                 fg="#b86d6d", bg="#faf3e0").pack(pady=(0, 10))

        # Crear Treeview
        columns = ("ID", "Nombre", "Emoji")
        self.tabla_emociones = ttk.Treeview(tabla_frame, columns=columns, show="headings", height=8)

        # Configurar columnas
        self.tabla_emociones.heading("ID", text="ID")
        self.tabla_emociones.heading("Nombre", text="Nombre")
        self.tabla_emociones.heading("Emoji", text="Emoji")

        self.tabla_emociones.column("ID", width=50)
        self.tabla_emociones.column("Nombre", width=150)
        self.tabla_emociones.column("Emoji", width=80)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla_emociones.yview)
        self.tabla_emociones.configure(yscrollcommand=scrollbar.set)

        self.tabla_emociones.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind evento de selección
        self.tabla_emociones.bind("<<TreeviewSelect>>", self.seleccionar_emocion_tabla)

    # -------- FUNCIONES DE LA VISTA -----------
    def seleccionar_imagen_emocion(self):
        filepath = filedialog.askopenfilename(
            title="Seleccionar imagen para la Emoción",
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")]
        )
        if filepath and self.validar_imagen(filepath):
            self.imagen_emocion_path.set(filepath)

    def validar_imagen(self, filepath):
        if not filepath:
            return True
        try:
            img = Image.open(filepath)
            if img.format not in ["JPEG", "PNG", "GIF"]:
                messagebox.showerror("Error", "Formato de imagen no soportado")
                return False
            if img.width > 1920 or img.height > 1080:
                messagebox.showwarning("Advertencia", "Imagen muy grande.")
                return True
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Imagen Inválida: {e}")
            return False

    def seleccionar_emocion_tabla(self, event):
        selected = self.tabla_emociones.focus()
        if selected:
            values = self.tabla_emociones.item(selected, 'values')
            self.limpiar_campos()
            self.emocion_id_entry.insert(0, values[0])
            self.nombre_emocion_entry.insert(0, values[1])

    # -------- MÉTODOS QUE LLAMAN AL CONTROLADOR -----------
    def guardar_emocion(self):
        if not self.validar_id_emocion():
            return

        nombre = self.nombre_emocion_entry.get()
        imagen = self.imagen_emocion_path.get().strip()

        if imagen and not self.validar_imagen(imagen):
            return

        if not self.validar_texto_nombre_emocion(nombre):
            return

        if messagebox.askyesno("Confirmar", f"¿Guardar emoción {nombre}?"):
            self.controller.guardar_emocion(nombre, imagen)

    def actualizar_emocion(self):
        emocion_id = self.emocion_id_entry.get()
        if not emocion_id:
            messagebox.showwarning("Advertencia", "ID de la emoción es obligatorio")
            return
        if not self.validar_id_emocion():
            return

        nombre = self.nombre_emocion_entry.get()

        if not self.validar_texto_nombre_emocion(nombre):
            return

        if messagebox.askyesno("Confirmar", f"¿Actualizar emoción con ID {emocion_id}?"):
            self.controller.actualizar_emocion(emocion_id, nombre)

    def eliminar_emocion(self):
        emocion_id = self.emocion_id_entry.get()
        if not emocion_id:
            messagebox.showwarning("Advertencia", "ID de la emoción es obligatorio")
            return
        if not self.validar_id_emocion():
            return

        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta emoción?"):
            self.controller.eliminar_emocion(emocion_id)

    def cargar_emociones(self):
        self.controller.cargar_emociones()

    def limpiar_campos(self):
        self.emocion_id_entry.delete(0, tk.END)
        self.nombre_emocion_entry.delete(0, tk.END)
        self.imagen_emocion_path.set("")

    # -------- VALIDACIONES -----------
    def validar_id_emocion(self):
        emocion = self.emocion_id_entry.get()
        if emocion and not emocion.isdigit():
            messagebox.showerror("Error", "ID Emoción debe ser un número")
            return False
        return True

    def validar_texto_nombre_emocion(self, texto):
        if not texto:
            messagebox.showerror("Error", "Nombre de la emoción es obligatorio")
            return False
        if not (1 <= len(texto) <= 50):
            messagebox.showerror("Error", "Nombre debe tener entre 1 y 50 caracteres")
            return False
        return True

    # -------- MÉTODOS PARA ACTUALIZAR LA VISTA -----------
    def actualizar_tabla(self, emociones):
        # Limpiar tabla
        for item in self.tabla_emociones.get_children():
            self.tabla_emociones.delete(item)

        # Insertar datos
        for emocion in emociones:
            self.tabla_emociones.insert("", "end", values=emocion)

    def mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        if tipo == "info":
            messagebox.showinfo(titulo, mensaje)
        elif tipo == "error":
            messagebox.showerror(titulo, mensaje)
        elif tipo == "warning":
            messagebox.showwarning(titulo, mensaje)