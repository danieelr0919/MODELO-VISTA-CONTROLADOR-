import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re
from PIL import Image

class UsuarioView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.setup_ui()
    
    def setup_ui(self):
        # Título
        titulo = tk.Label(self.parent, text="👤 Gestión de Usuarios", font=("Arial", 16, "bold"), fg="#b86d6d",
                          bg="#faf3e0")
        titulo.pack(pady=(20, 10))

        # Frame del formulario
        form_frame = tk.Frame(self.parent, bg="#f8f0e3", padx=20, pady=20, relief="groove", bd=1)
        form_frame.pack(pady=10, padx=20, fill="x")

        # Campos del formulario
        tk.Label(form_frame, text="ID Usuario:", bg="#f8f0e3", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        self.usuario_id_entry = tk.Entry(form_frame, width=30)
        self.usuario_id_entry.grid(row=0, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Username:", bg="#f8f0e3", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(form_frame, width=30)
        self.username_entry.grid(row=1, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Email:", bg="#f8f0e3", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
        self.email_entry = tk.Entry(form_frame, width=30)
        self.email_entry.grid(row=2, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Contraseña:", bg="#f8f0e3", font=("Arial", 12)).grid(row=3, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(form_frame, width=30, show="*")
        self.password_entry.grid(row=3, column=1, sticky="w", pady=5)

        # Campo de imagen
        tk.Label(form_frame, text="Imagen de Perfil:", bg="#f8f0e3", font=("Arial", 12)).grid(row=4, column=0, sticky="w", pady=5)
        self.imagen_path = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.imagen_path, width=30).grid(row=4, column=1, sticky="w", pady=5)
        tk.Button(form_frame, text="Seleccionar Imagen", command=self.seleccionar_imagen).grid(row=4, column=2, sticky="w", pady=5)

        # Botones
        btn_frame = tk.Frame(self.parent, bg="#faf3e0")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="💾 Guardar", bg="#88c9a1", fg="white", width=12,
                  command=self.guardar_usuario).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✏️ Actualizar", bg="#a2b9bc", fg="white", width=12,
                  command=self.actualizar_usuario).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑️ Eliminar", bg="#e77f67", fg="white", width=12,
                  command=self.eliminar_usuario).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🧹 Limpiar", bg="#f5c091", fg="#5a4a42", width=12,
                  command=self.limpiar_campos).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🔄 Cargar Datos", bg="#a2b9bc", fg="white", width=12,
                  command=self.cargar_usuarios).pack(side=tk.LEFT, padx=5)

        # Botones de exportación
        export_frame = tk.Frame(btn_frame, bg="#faf3e0")
        export_frame.pack(side=tk.LEFT, padx=10)

        tk.Label(export_frame, text="Exportar:", bg="#faf3e0", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Button(export_frame, text="📊 Excel", bg="#5B9BD5", fg="white", width=8,
                  command=self.exportar_excel).pack(side=tk.LEFT, padx=2)
        tk.Button(export_frame, text="📄 PDF", bg="#ED7D31", fg="white", width=8,
                  command=self.exportar_pdf).pack(side=tk.LEFT, padx=2)

        # TABLA DE USUARIOS
        tabla_frame = tk.Frame(self.parent, bg="#faf3e0")
        tabla_frame.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Label(tabla_frame, text="📋 Lista de Usuarios", font=("Arial", 14, "bold"),
                 fg="#b86d6d", bg="#faf3e0").pack(pady=(0, 10))

        # Crear Treeview
        columns = ("ID", "Username", "Email", "Fecha Registro")
        self.tabla_usuarios = ttk.Treeview(tabla_frame, columns=columns, show="headings", height=8)

        # Configurar columnas
        self.tabla_usuarios.heading("ID", text="ID")
        self.tabla_usuarios.heading("Username", text="Username")
        self.tabla_usuarios.heading("Email", text="Email")
        self.tabla_usuarios.heading("Fecha Registro", text="Fecha Registro")

        self.tabla_usuarios.column("ID", width=50)
        self.tabla_usuarios.column("Username", width=120)
        self.tabla_usuarios.column("Email", width=150)
        self.tabla_usuarios.column("Fecha Registro", width=120)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla_usuarios.yview)
        self.tabla_usuarios.configure(yscrollcommand=scrollbar.set)

        self.tabla_usuarios.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind evento de selección
        self.tabla_usuarios.bind("<<TreeviewSelect>>", self.seleccionar_usuario_tabla)

    # -------- MÉTODOS QUE LLAMAN AL CONTROLADOR -----------
    def guardar_usuario(self):
        print("DEBUG: Botón guardar_usuario presionado")
        
        if not self.validar_id_usuario():
            print("DEBUG: Validación de ID falló")
            return

        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        print(f"DEBUG: Datos capturados - username: {username}, email: {email}, password: {password}")

        if not self.validar_texto_username(username):
            print("DEBUG: Validación de username falló")
            return
        if not self.validar_email_usuario(email):
            print("DEBUG: Validación de email falló")
            return
        if not self.validar_texto_password(password):
            print("DEBUG: Validación de password falló")
            return

        if messagebox.askyesno("Confirmar", f"¿Guardar usuario {username}?"):
            print("DEBUG: Confirmación aceptada, llamando al controlador")
            self.controller.guardar_usuario(username, email, password)
        else:
            print("DEBUG: Usuario canceló la operación")

    def actualizar_usuario(self):
        user_id = self.usuario_id_entry.get()
        if not user_id:
            messagebox.showwarning("Advertencia", "ID de usuario es obligatorio")
            return
        if not self.validar_id_usuario():
            return

        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not self.validar_texto_username(username):
            return
        if not self.validar_email_usuario(email):
            return

        if messagebox.askyesno("Confirmar", f"¿Actualizar usuario con ID {user_id}?"):
            self.controller.actualizar_usuario(user_id, username, email, password)

    def eliminar_usuario(self):
        user_id = self.usuario_id_entry.get()
        if not user_id:
            messagebox.showwarning("Advertencia", "ID de usuario es obligatorio")
            return
        if not self.validar_id_usuario():
            return

        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este usuario?"):
            self.controller.eliminar_usuario(user_id)

    def cargar_usuarios(self):
        self.controller.cargar_usuarios()

    def limpiar_campos(self):
        self.usuario_id_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    # -------- VALIDACIONES -----------
    def validar_id_usuario(self):
        usuario_id = self.usuario_id_entry.get()
        if usuario_id and not usuario_id.isdigit():
            messagebox.showerror("Error", "ID Usuario debe ser un número")
            return False
        return True

    def validar_texto_username(self, texto):
        if not texto:
            messagebox.showerror("Error", "Username es obligatorio")
            return False
        if not (4 <= len(texto) <= 50):
            messagebox.showerror("Error", "Username debe tener entre 4 y 50 caracteres")
            return False
        return True

    def validar_texto_password(self, texto):
        if not texto:
            messagebox.showerror("Error", "Contraseña es obligatoria")
            return False
        if len(texto) < 6:
            messagebox.showerror("Error", "Contraseña debe tener al menos 6 caracteres")
            return False
        return True

    def validar_email_usuario(self, email):
        if not email:
            messagebox.showerror("Error", "Email es obligatorio")
            return False
        # Validación básica de formato de email
        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Formato de email inválido")
            return False
        return True

    def seleccionar_usuario_tabla(self, event):
        selected = self.tabla_usuarios.focus()
        if selected:
            values = self.tabla_usuarios.item(selected, 'values')
            self.limpiar_campos()
            self.usuario_id_entry.insert(0, values[0])
            self.username_entry.insert(0, values[1])
            self.email_entry.insert(0, values[2])

    # -------- FUNCIONES DE LA VISTA -----------
    def seleccionar_imagen(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")])
        if filepath and self.validar_imagen(filepath):
            self.imagen_path.set(filepath)

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

    # -------- MÉTODOS PARA ACTUALIZAR LA VISTA -----------
    def actualizar_tabla(self, usuarios):
        # Limpiar tabla
        for item in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(item)
        
        # Insertar datos
        for usuario in usuarios:
            self.tabla_usuarios.insert("", "end", values=usuario)

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
            usuarios = []
            for item in self.tabla_usuarios.get_children():
                usuarios.append(self.tabla_usuarios.item(item)['values'])
            
            if usuarios:
                # Llamar al exportador con el formato correcto
                success = exportador.exportar_excel("usuarios", usuarios)
                # El mensaje ya se muestra dentro del exportador
            else:
                self.mostrar_mensaje("Advertencia", "No hay usuarios para exportar", "warning")
        except Exception as e:
            self.mostrar_mensaje("Error", f"No se pudo exportar: {e}", "error")

    def exportar_pdf(self):
        try:
            from exportadores.exportador_central import ExportadorCentral
            exportador = ExportadorCentral()
            
            # Obtener datos de la tabla
            usuarios = []
            for item in self.tabla_usuarios.get_children():
                usuarios.append(self.tabla_usuarios.item(item)['values'])
            
            if usuarios:
                # Llamar al exportador con el formato correcto
                success = exportador.exportar_pdf("usuarios", usuarios)
                # El mensaje ya se muestra dentro del exportador
            else:
                self.mostrar_mensaje("Advertencia", "No hay usuarios para exportar", "warning")
        except Exception as e:
            self.mostrar_mensaje("Error", f"No se pudo exportar: {e}", "error")