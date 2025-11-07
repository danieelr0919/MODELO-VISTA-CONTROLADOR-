from tkinter import messagebox, filedialog, Toplevel, Label, Entry, Button, Frame
from datetime import datetime

from exportadores.excel.usuarios_excel import UsuariosExcelExporter
from exportadores.excel.emociones_excel import EmocionesExcelExporter
from exportadores.excel.entradas_excel import EntradasExcelExporter
from exportadores.excel.reportes_excel import ReportesExcelExporter
from exportadores.pdf.usuarios_pdf import UsuariosPDFExporter
from exportadores.pdf.emociones_pdf import EmocionesPDFExporter
from exportadores.pdf.entradas_pdf import EntradasPDFExporter
from exportadores.pdf.reportes_pdf import ReportesPDFExporter

class ExportadorCentral:
    def __init__(self):
        # Inicializar todos los exportadores
        self.excel_exporters = {
            'usuarios': UsuariosExcelExporter(),
            'emociones': EmocionesExcelExporter(),
            'entradas': EntradasExcelExporter(),
            'reportes': ReportesExcelExporter()
        }
        
        self.pdf_exporters = {
            'usuarios': UsuariosPDFExporter(),
            'emociones': EmocionesPDFExporter(),
            'entradas': EntradasPDFExporter(),
            'reportes': ReportesPDFExporter()
        }
        
        self.ultimo_reporte = None
    
    def mostrar_filtros_exportacion(self, modulo, datos, callback):
        """Mostrar ventana de filtros para exportación"""
        filtro_window = Toplevel()
        filtro_window.title(f"Filtros de Exportación - {modulo.title()}")
        filtro_window.geometry("400x300")
        filtro_window.configure(bg="#faf3e0")
        
        # Frame principal
        main_frame = Frame(filtro_window, bg="#faf3e0", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        Label(main_frame, text=f"Filtros para {modulo.title()}", 
              font=("Arial", 14, "bold"), bg="#faf3e0", fg="#b86d6d").pack(pady=10)
        
        # Filtros específicos por módulo
        filtros_frame = Frame(main_frame, bg="#f8f0e3", padx=10, pady=10)
        filtros_frame.pack(fill="x", pady=10)
        
        filtros = {}
        
        if modulo == "entradas":
            # Filtros para entradas
            Label(filtros_frame, text="Rango de Fechas:", bg="#f8f0e3").grid(row=0, column=0, sticky="w", pady=5)
            
            Label(filtros_frame, text="Fecha Inicio (YYYY-MM-DD):", bg="#f8f0e3", font=("Arial", 9)).grid(row=1, column=0, sticky="w")
            filtros['fecha_inicio'] = Entry(filtros_frame, width=15)
            filtros['fecha_inicio'].grid(row=1, column=1, sticky="w", padx=5)
            
            Label(filtros_frame, text="Fecha Fin (YYYY-MM-DD):", bg="#f8f0e3", font=("Arial", 9)).grid(row=2, column=0, sticky="w")
            filtros['fecha_fin'] = Entry(filtros_frame, width=15)
            filtros['fecha_fin'].grid(row=2, column=1, sticky="w", padx=5)
            
            Label(filtros_frame, text="ID Usuario:", bg="#f8f0e3").grid(row=3, column=0, sticky="w", pady=5)
            filtros['usuario_id'] = Entry(filtros_frame, width=15)
            filtros['usuario_id'].grid(row=3, column=1, sticky="w", padx=5)
            
        elif modulo == "reportes":
            # Filtros para reportes
            Label(filtros_frame, text="Período:", bg="#f8f0e3").grid(row=0, column=0, sticky="w", pady=5)
            filtros['periodo'] = Entry(filtros_frame, width=15)
            filtros['periodo'].insert(0, "mes")
            filtros['periodo'].grid(row=0, column=1, sticky="w", padx=5)
            
            Label(filtros_frame, text="Emoción específica:", bg="#f8f0e3").grid(row=1, column=0, sticky="w", pady=5)
            filtros['emocion'] = Entry(filtros_frame, width=15)
            filtros['emocion'].grid(row=1, column=1, sticky="w", padx=5)
            
        elif modulo == "usuarios":
            # Filtros para usuarios
            Label(filtros_frame, text="Fecha Registro Desde:", bg="#f8f0e3").grid(row=0, column=0, sticky="w", pady=5)
            filtros['fecha_registro'] = Entry(filtros_frame, width=15)
            filtros['fecha_registro'].grid(row=0, column=1, sticky="w", padx=5)
            
        # Botones
        btn_frame = Frame(main_frame, bg="#faf3e0")
        btn_frame.pack(pady=20)
        
        Button(btn_frame, text="📊 Exportar con Filtros", bg="#5B9BD5", fg="white",
               command=lambda: self.aplicar_filtros_y_exportar(modulo, datos, filtros, callback, filtro_window)).pack(side="left", padx=5)
        
        Button(btn_frame, text="📄 Exportar Todo", bg="#ED7D31", fg="white",
               command=lambda: self.exportar_todo(modulo, datos, callback, filtro_window)).pack(side="left", padx=5)
        
        Button(btn_frame, text="❌ Cancelar", bg="#e77f67", fg="white",
               command=filtro_window.destroy).pack(side="left", padx=5)
    
    def aplicar_filtros_y_exportar(self, modulo, datos, filtros, callback, ventana):
        """Aplicar filtros y proceder con la exportación"""
        try:
            datos_filtrados = self.aplicar_filtros(modulo, datos, filtros)
            ventana.destroy()
            callback(modulo, datos_filtrados, True)  # True indica que son datos filtrados
        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar filtros: {e}")
    
    def exportar_todo(self, modulo, datos, callback, ventana):
        """Exportar todos los datos sin filtros"""
        ventana.destroy()
        callback(modulo, datos, False)  # False indica datos completos
    
    def aplicar_filtros(self, modulo, datos, filtros):
        """Aplicar filtros a los datos según el módulo"""
        if not datos:
            return datos
        
        datos_filtrados = datos.copy()
        
        if modulo == "entradas":
            # Filtrar por rango de fechas
            fecha_inicio = filtros['fecha_inicio'].get().strip()
            fecha_fin = filtros['fecha_fin'].get().strip()
            usuario_id = filtros['usuario_id'].get().strip()
            
            if fecha_inicio:
                try:
                    fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
                    datos_filtrados = [d for d in datos_filtrados if len(d) > 2 and d[2] >= fecha_inicio]
                except ValueError:
                    messagebox.showerror("Error", "Formato de fecha inicio inválido. Use YYYY-MM-DD")
                    return datos
            
            if fecha_fin:
                try:
                    fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
                    datos_filtrados = [d for d in datos_filtrados if len(d) > 2 and d[2] <= fecha_fin]
                except ValueError:
                    messagebox.showerror("Error", "Formato de fecha fin inválido. Use YYYY-MM-DD")
                    return datos
            
            if usuario_id:
                datos_filtrados = [d for d in datos_filtrados if len(d) > 1 and str(d[1]) == usuario_id]
                
        elif modulo == "reportes":
            # Filtrar por emoción específica
            emocion = filtros['emocion'].get().strip()
            if emocion:
                datos_filtrados = [d for d in datos_filtrados if len(d) > 0 and emocion.lower() in str(d[0]).lower()]
        
        return datos_filtrados
    
    def exportar_excel(self, modulo, datos, usuario_id=None, con_filtros=False):
        """Exportar cualquier módulo a Excel con opción de filtros"""
        try:
            if not datos:
                messagebox.showwarning("Advertencia", f"No hay datos en {modulo} para exportar")
                return False
            
            # Mostrar filtros primero si no se han aplicado
            if not con_filtros and modulo in ["entradas", "reportes", "usuarios"]:
                self.mostrar_filtros_exportacion(modulo, datos, self._exportar_excel_despues_filtros)
                return True
            
            # Continuar con exportación normal
            return self._exportar_excel_directo(modulo, datos)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar {modulo} a Excel: {e}")
            return False
    
    def _exportar_excel_despues_filtros(self, modulo, datos_filtrados, con_filtros):
        """Callback después de aplicar filtros"""
        if datos_filtrados:
            self._exportar_excel_directo(modulo, datos_filtrados, con_filtros)
        else:
            messagebox.showwarning("Advertencia", "No hay datos que coincidan con los filtros aplicados")
    
    def _exportar_excel_directo(self, modulo, datos, con_filtros=False):
        """Exportación directa a Excel"""
        # Mapear nombres de archivo
        nombres_archivo = {
            "usuarios": "reporte_usuarios",
            "emociones": "catalogo_emociones", 
            "entradas": "historial_entradas",
            "reportes": "reporte_emocional"
        }
        
        sufijo = "_filtrado" if con_filtros else ""
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title=f"Guardar {modulo} como Excel",
            initialfile=f"{nombres_archivo.get(modulo, 'reporte')}{sufijo}.xlsx"
        )
        
        if filename and modulo in self.excel_exporters:
            self.excel_exporters[modulo].exportar(datos, filename)
            messagebox.showinfo("Éxito", f"{modulo.title()} exportados a Excel:\n{filename}")
            return True
        return False
    
    def exportar_pdf(self, modulo, datos, usuario_id=None, con_filtros=False):
        """Exportar cualquier módulo a PDF con opción de filtros"""
        try:
            if not datos:
                messagebox.showwarning("Advertencia", f"No hay datos en {modulo} para exportar")
                return False
            
            # Mostrar filtros primero si no se han aplicado
            if not con_filtros and modulo in ["entradas", "reportes", "usuarios"]:
                self.mostrar_filtros_exportacion(modulo, datos, self._exportar_pdf_despues_filtros)
                return True
            
            # Continuar con exportación normal
            return self._exportar_pdf_directo(modulo, datos)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar {modulo} a PDF: {e}")
            return False
    
    def _exportar_pdf_despues_filtros(self, modulo, datos_filtrados, con_filtros):
        """Callback después de aplicar filtros para PDF"""
        if datos_filtrados:
            self._exportar_pdf_directo(modulo, datos_filtrados, con_filtros)
        else:
            messagebox.showwarning("Advertencia", "No hay datos que coincidan con los filtros aplicados")
    
    def _exportar_pdf_directo(self, modulo, datos, con_filtros=False):
        """Exportación directa a PDF"""
        nombres_archivo = {
            "usuarios": "reporte_usuarios",
            "emociones": "catalogo_emociones",
            "entradas": "historial_entradas", 
            "reportes": "reporte_emocional"
        }
        
        sufijo = "_filtrado" if con_filtros else ""
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title=f"Guardar {modulo} como PDF",
            initialfile=f"{nombres_archivo.get(modulo, 'reporte')}{sufijo}.pdf"
        )
        
        if filename and modulo in self.pdf_exporters:
            self.pdf_exporters[modulo].exportar(datos, filename)
            messagebox.showinfo("Éxito", f"{modulo.title()} exportados a PDF:\n{filename}")
            return True
        return False
    
    def set_reporte_actual(self, reporte_data):
        """Guardar el reporte actual para exportación"""
        self.ultimo_reporte = reporte_data