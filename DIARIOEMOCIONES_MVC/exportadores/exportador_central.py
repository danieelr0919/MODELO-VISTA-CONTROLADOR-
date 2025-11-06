from tkinter import messagebox, filedialog


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
    
    def exportar_excel(self, modulo, datos, usuario_id=None):
        """Exportar cualquier módulo a Excel"""
        try:
            if not datos:
                messagebox.showwarning("Advertencia", f"No hay datos en {modulo} para exportar")
                return False
            
            # Mapear nombres de archivo
            nombres_archivo = {
                "usuarios": "reporte_usuarios",
                "emociones": "catalogo_emociones", 
                "entradas": "historial_entradas",
                "reportes": "reporte_emocional"
            }
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title=f"Guardar {modulo} como Excel",
                initialfile=f"{nombres_archivo.get(modulo, 'reporte')}.xlsx"
            )
            
            if filename and modulo in self.excel_exporters:
                self.excel_exporters[modulo].exportar(datos, filename)
                messagebox.showinfo("Éxito", f"{modulo.title()} exportados a Excel:\n{filename}")
                return True
            return False
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar {modulo} a Excel: {e}")
            return False
    
    def exportar_pdf(self, modulo, datos, usuario_id=None):
        """Exportar cualquier módulo a PDF"""
        try:
            if not datos:
                messagebox.showwarning("Advertencia", f"No hay datos en {modulo} para exportar")
                return False
            
            nombres_archivo = {
                "usuarios": "reporte_usuarios",
                "emociones": "catalogo_emociones",
                "entradas": "historial_entradas", 
                "reportes": "reporte_emocional"
            }
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                title=f"Guardar {modulo} como PDF",
                initialfile=f"{nombres_archivo.get(modulo, 'reporte')}.pdf"
            )
            
            if filename and modulo in self.pdf_exporters:
                self.pdf_exporters[modulo].exportar(datos, filename)
                messagebox.showinfo("Éxito", f"{modulo.title()} exportados a PDF:\n{filename}")
                return True
            return False
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar {modulo} a PDF: {e}")
            return False
    
    def set_reporte_actual(self, reporte_data):
        """Guardar el reporte actual para exportación"""
        self.ultimo_reporte = reporte_data