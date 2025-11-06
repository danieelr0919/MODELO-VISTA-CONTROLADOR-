import tkinter as tk
from tkinter import ttk, messagebox

class ReporteView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.crear_interfaz()
    
    def crear_interfaz(self):
        titulo = tk.Label(self.parent, text="📈 Resumen Emocional", font=("Arial", 16, "bold"), fg="#b86d6d",
                          bg="#faf3e0")
        titulo.pack(pady=(20, 10))

        form_frame = tk.Frame(self.parent, bg="#f8f0e3", padx=20, pady=20, relief="groove", bd=1)
        form_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(form_frame, text="Selecciona un usuario (ID):", bg="#f8f0e3", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        self.reporte_usuario_id_entry = tk.Entry(form_frame, width=30)
        self.reporte_usuario_id_entry.grid(row=0, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Período:", bg="#f8f0e3", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.periodo_var = tk.StringVar(value="semana")
        ttk.Radiobutton(form_frame, text="Semana", variable=self.periodo_var, value="semana").grid(row=1, column=1, sticky="w")
        ttk.Radiobutton(form_frame, text="Mes", variable=self.periodo_var, value="mes").grid(row=1, column=2, sticky="w")

        btn_frame = tk.Frame(self.parent, bg="#faf3e0")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="📊 Generar Reporte", bg="#88c9a1", fg="white", width=20,
                  command=self.generar_reporte).pack(padx=5)

        # TABLA DE REPORTES
        tabla_frame = tk.Frame(self.parent, bg="#faf3e0")
        tabla_frame.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Label(tabla_frame, text="📊 Estadísticas Emocionales", font=("Arial", 14, "bold"),
                 fg="#b86d6d", bg="#faf3e0").pack(pady=(0, 10))

        # Crear Treeview para reportes
        columns = ("Emoción", "Frecuencia", "Última Registro")
        self.tabla_reportes = ttk.Treeview(tabla_frame, columns=columns, show="headings", height=8)

        # Configurar columnas
        self.tabla_reportes.heading("Emoción", text="Emoción")
        self.tabla_reportes.heading("Frecuencia", text="Frecuencia")
        self.tabla_reportes.heading("Última Registro", text="Última Registro")

        self.tabla_reportes.column("Emoción", width=150)
        self.tabla_reportes.column("Frecuencia", width=100)
        self.tabla_reportes.column("Última Registro", width=120)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla_reportes.yview)
        self.tabla_reportes.configure(yscrollcommand=scrollbar.set)

        self.tabla_reportes.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # -------- MÉTODOS QUE LLAMAN AL CONTROLADOR -----------
    def generar_reporte(self):
        usuario_id = self.reporte_usuario_id_entry.get()
        periodo = self.periodo_var.get()

        if not usuario_id:
            messagebox.showwarning("Advertencia", "Por favor, Ingrese un ID de usuario para generar reporte")
            return
        if not usuario_id.isdigit():
            messagebox.showerror("Error", "ID de usuario debe ser un número")
            return

        self.controller.generar_reporte(usuario_id, periodo)

    # -------- MÉTODOS PARA ACTUALIZAR LA VISTA -----------
    def actualizar_tabla(self, resultados):
        # Limpiar tabla
        for item in self.tabla_reportes.get_children():
            self.tabla_reportes.delete(item)

        # Insertar datos en la tabla
        if resultados:
            for emocion, frecuencia, ultima_fecha in resultados:
                self.tabla_reportes.insert("", "end", values=(emocion, f"{frecuencia} veces", ultima_fecha))
        else:
            messagebox.showinfo("Reporte", "No hay datos para generar el reporte")

    def mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        if tipo == "info":
            messagebox.showinfo(titulo, mensaje)
        elif tipo == "error":
            messagebox.showerror(titulo, mensaje)
        elif tipo == "warning":
            messagebox.showwarning(titulo, mensaje)