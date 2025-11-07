from fpdf import FPDF
from datetime import datetime

class EmocionesPDFExporter:
    def exportar(self, datos, filename):
        """Exportar emociones a PDF con formato profesional"""
        pdf = FPDF()
        pdf.add_page()
        
        # Configuración
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Título
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "CATÁLOGO DE EMOCIONES", 0, 1, 'C')
        pdf.ln(5)
        
        # Información del reporte
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 8, f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1)
        pdf.cell(0, 8, f"Total de emociones: {len(datos)}", 0, 1)
        pdf.ln(10)
        
        # Encabezados de tabla
        pdf.set_fill_color(198, 89, 17)  # Naranja
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", 'B', 12)
        
        # Anchos de columna
        widths = [15, 50, 20]
        headers = ["ID", "Nombre", "Emoji"]
        
        for i, header in enumerate(headers):
            pdf.cell(widths[i], 10, header, 1, 0, 'C', True)
        pdf.ln()
        
        # Datos
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", '', 10)
        
        for emocion in datos:
            for i, valor in enumerate(emocion):
                pdf.cell(widths[i], 10, str(valor), 1, 0, 'C')
            pdf.ln()
        
        # Guardar
        pdf.output(filename)