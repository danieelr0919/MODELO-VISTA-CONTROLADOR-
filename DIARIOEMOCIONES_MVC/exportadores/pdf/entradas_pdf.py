from fpdf import FPDF
from datetime import datetime

class EntradasPDFExporter:
    def exportar(self, datos, filename):
        """Exportar entradas a PDF con formato profesional"""
        pdf = FPDF()
        pdf.add_page()
        
        # Configuración
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Título
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "HISTORIAL DE ENTRADAS", 0, 1, 'C')
        pdf.ln(5)
        
        # Información del reporte
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 8, f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1)
        pdf.cell(0, 8, f"Total de entradas: {len(datos)}", 0, 1)
        pdf.ln(10)
        
        # Encabezados de tabla
        pdf.set_fill_color(112, 173, 71)  # Verde
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", 'B', 12)
        
        # Anchos de columna
        widths = [15, 25, 25, 125]
        headers = ["ID", "Usuario", "Fecha", "Resumen"]
        
        for i, header in enumerate(headers):
            pdf.cell(widths[i], 10, header, 1, 0, 'C', True)
        pdf.ln()
        
        # Datos
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", '', 9)
        
        for entrada in datos:
            # ID
            pdf.cell(widths[0], 10, str(entrada[0]), 1, 0, 'C')
            # Usuario
            pdf.cell(widths[1], 10, str(entrada[1]), 1, 0, 'C')
            # Fecha
            pdf.cell(widths[2], 10, str(entrada[2]), 1, 0, 'C')
            # Texto (truncado para mejor visualización)
            texto = str(entrada[3]) if len(entrada) > 3 else ""
            if len(texto) > 60:
                texto = texto[:57] + "..."
            pdf.cell(widths[3], 10, texto, 1, 0, 'L')
            pdf.ln()
        
        # Guardar
        pdf.output(filename)