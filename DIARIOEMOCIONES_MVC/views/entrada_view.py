import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

class EntradaView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Título
        titulo = tk.Label(self.parent, text="📖 Entradas del Diario", font=("Arial", 16, "bold"), fg="#b86d6d",
                          bg="#faf3e0")
        titulo.pack(pady=(20, 10))

        # Frame del formulario
        form_frame = tk.Frame(self.parent, bg="#f8f0e3", padx=20, pady=20, relief="groove", bd=1)
        form_frame.pack(pady=10, padx=20, fill="x")

        # Campos del formulario
        tk.Label(form_frame, text="ID Entrada:", bg="#f8f0e3", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        self.entrada_id_entry = tk.Entry(form_frame, width=30)
        self.entrada_id_entry.grid(row=0, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Usuario ID:", bg="#f8f0e3", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.entrada_usuario_id_entry = tk.Entry(form_frame, width=30)
        self.entrada_usuario_id_entry.grid(row=1, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Fecha:", bg="#f8f0e3", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
        self.fecha_entry = DateEntry(form_frame, width=28, date_pattern="yyyy-mm-dd")
        self.fecha_entry.grid(row=2, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Texto:", bg="#f8f0e3", font=("Arial", 12)).grid(row=3, column=0, sticky="nw", pady=5)
        self.texto_entry = tk.Text(form_frame, width=30, height=5)
        self.texto_entry.grid(row=3, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Emociones (IDs):", bg="#f8f0e3", font=("Arial", 12)).grid(row=4, column=0, sticky="w", pady=5)
        self.emociones_ids_entry = tk.Entry(form_frame, width=30)
        self.emociones_ids_entry.grid(row=4, column=1, sticky="w", pady=5)

        # Botones
        btn_frame = tk.Frame(self.parent, bg="#faf3e0")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="💾 Guardar", bg="#88c9a1", fg="white", width=12,
                  command=self.guardar_entrada).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✏️ Actualizar", bg="#a2b9bc", fg="white", width=12,
                  command=self.actualizar_entrada).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑️ Eliminar", bg="#e77f67", fg="white", width=12,
                  command=self.eliminar_entrada).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🧹 Limpiar", bg="#f5c091", fg="#5a4a42", width=12,
                  command=self.limpiar_campos).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🔄 Cargar Datos", bg="#a2b9bc", fg="white", width=12,
                  command=self.cargar_entradas).pack(side=tk.LEFT, padx=5)

        # Botones de exportación
        export_frame = tk.Frame(btn_frame, bg="#faf3e0")
        export_frame.pack(side=tk.LEFT, padx=10)

        tk.Label(export_frame, text="Exportar:", bg="#faf3e0", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(export_frame, text="📊 Excel", bg="#5B9BD5", fg="white", width=8,
                  command=self.exportar_excel).pack(side=tk.LEFT, padx=2)
        tk.Button(export_frame, text="📄 PDF", bg="#ED7D31", fg="white", width=8,
                  command=self.exportar_pdf).pack(side=tk.LEFT, padx=2)

        # TABLA DE ENTRADAS
        tabla_frame = tk.Frame(self.parent, bg="#faf3e0")
        tabla_frame.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Label(tabla_frame, text="📋 Historial de Entradas", font=("Arial", 14, "bold"),
                 fg="#b86d6d", bg="#faf3e0").pack(pady=(0, 10))

        # Crear Treeview
        columns = ("ID", "Usuario", "Fecha", "Resumen")
        self.tabla_entradas = ttk.Treeview(tabla_frame, columns=columns, show="headings", height=8)

        # Configurar columnas
        self.tabla_entradas.heading("ID", text="ID")
        self.tabla_entradas.heading("Usuario", text="Usuario")
        self.tabla_entradas.heading("Fecha", text="Fecha")
        self.tabla_entradas.heading("Resumen", text="Resumen")

        self.tabla_entradas.column("ID", width=50)
        self.tabla_entradas.column("Usuario", width=100)
        self.tabla_entradas.column("Fecha", width=100)
        self.tabla_entradas.column("Resumen", width=200)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla_entradas.yview)
        self.tabla_entradas.configure(yscrollcommand=scrollbar.set)

        self.tabla_entradas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind evento de selección
        self.tabla_entradas.bind("<<TreeviewSelect>>", self.seleccionar_entrada_tabla)

    # -------- MÉTODOS QUE LLAMAN AL CONTROLADOR -----------
    def guardar_entrada(self):
        if not self.validar_usuario_id_entrada():
            return

        usuario_id = self.entrada_usuario_id_entry.get()
        fecha = self.fecha_entry.get()
        texto = self.texto_entry.get("1.0", tk.END).strip()
        emociones_ids = self.emociones_ids_entry.get()

        if not self.validar_entrada(texto):
            return

        if messagebox.askyesno("Confirmar", f"¿Guardar entrada para Usuario {usuario_id}?"):
            self.controller.guardar_entrada(usuario_id, fecha, texto, emociones_ids)

    def actualizar_entrada(self):
        entrada_id = self.entrada_id_entry.get()
        if not entrada_id:
            messagebox.showwarning("Advertencia", "ID de entrada es obligatorio")
            return
        if not self.validar_id_entrada():
            return

        usuario_id = self.entrada_usuario_id_entry.get()
        fecha = self.fecha_entry.get()
        texto = self.texto_entry.get("1.0", tk.END).strip()

        if not self.validar_usuario_id_entrada():
            return
        if not self.validar_entrada(texto):
            return

        if messagebox.askyesno("Confirmar", f"¿Actualizar entrada con ID {entrada_id}?"):
            self.controller.actualizar_entrada(entrada_id, usuario_id, fecha, texto)

    def eliminar_entrada(self):
        entrada_id = self.entrada_id_entry.get()
        if not entrada_id:
            messagebox.showwarning("Advertencia", "ID de entrada es obligatorio")
            return
        if not self.validar_id_entrada():
            return

        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta entrada?"):
            self.controller.eliminar_entrada(entrada_id)

    def cargar_entradas(self):
        self.controller.cargar_entradas()

    def limpiar_campos(self):
        self.entrada_id_entry.delete(0, tk.END)
        self.entrada_usuario_id_entry.delete(0, tk.END)
        self.fecha_entry.delete(0, tk.END)
        self.texto_entry.delete("1.0", tk.END)
        self.emociones_ids_entry.delete(0, tk.END)

    def seleccionar_entrada_tabla(self, event):
        selected = self.tabla_entradas.focus()
        if selected:
            values = self.tabla_entradas.item(selected, 'values')
            self.limpiar_campos()
            self.entrada_id_entry.insert(0, values[0])

    # -------- VALIDACIONES -----------
    def validar_id_entrada(self):
        entrada_id = self.entrada_id_entry.get()
        if entrada_id and not entrada_id.isdigit():
            messagebox.showerror("Error", "ID Entrada debe ser un número")
            return False
        return True

    def validar_usuario_id_entrada(self):
        usuario_id = self.entrada_usuario_id_entry.get()
        if usuario_id and not usuario_id.isdigit():
            messagebox.showerror("Error", "ID Usuario en Entradas debe ser un número")
            return False
        return True

    def validar_entrada(self, texto):
        if not texto or texto.strip() == "":
            messagebox.showerror("Error", "El texto de la entrada es obligatorio")
            return False
        return True

    # -------- MÉTODOS PARA ACTUALIZAR LA VISTA -----------
    def actualizar_tabla(self, entradas):
        # Limpiar tabla
        for item in self.tabla_entradas.get_children():
            self.tabla_entradas.delete(item)

        # Insertar datos
        for entrada in entradas:
            self.tabla_entradas.insert("", "end", values=entrada)

    def mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        if tipo == "info":
            messagebox.showinfo(titulo, mensaje)
        elif tipo == "error":
            messagebox.showerror(titulo, mensaje)
        elif tipo == "warning":
            messagebox.showwarning(titulo, mensaje)

    def exportar_excel(self):
        try:
            from exportadores.exportador_central import ExportadorCentral
            exportador = ExportadorCentral()
            
            # Obtener datos de la tabla
            entradas = []
            for item in self.tabla_entradas.get_children():
                entradas.append(self.tabla_entradas.item(item)['values'])
            
            if entradas:
                success = exportador.exportar_excel("entradas", entradas)
                # El mensaje ya se muestra dentro del exportador
            else:
                self.mostrar_mensaje("Advertencia", "No hay entradas para exportar", "warning")
        except Exception as e:
            self.mostrar_mensaje("Error", f"No se pudo exportar: {e}", "error")

    def exportar_pdf(self):
        try:
            from exportadores.exportador_central import ExportadorCentral
            exportador = ExportadorCentral()
            
            # Obtener datos de la tabla
            entradas = []
            for item in self.tabla_entradas.get_children():
                entradas.append(self.tabla_entradas.item(item)['values'])
            
            if entradas:
                success = exportador.exportar_pdf("entradas", entradas)
                # El mensaje ya se muestra dentro del exportador
            else:
                self.mostrar_mensaje("Advertencia", "No hay entradas para exportar", "warning")
        except Exception as e:
            self.mostrar_mensaje("Error", f"No se pudo exportar: {e}", "error")