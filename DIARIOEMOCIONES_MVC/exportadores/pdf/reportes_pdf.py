from fpdf import FPDF
from datetime import datetime

class ReportesPDFExporter:
    def exportar(self, datos, filename):
        """Exportar reportes a PDF con formato profesional"""
        pdf = FPDF()
        pdf.add_page()
        
        # Configuración
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Título
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "REPORTE EMOCIONAL - DIARIO DE EMOCIONES", 0, 1, 'C')
        pdf.ln(5)
        
        # Información del reporte
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 8, f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1)
        pdf.cell(0, 8, f"Total de emociones registradas: {len(datos)}", 0, 1)
        
        # Calcular estadísticas
        total_frecuencia = sum(int(str(d[1]).split()[0]) for d in datos if len(d) > 1)
        pdf.cell(0, 8, f"Total de registros emocionales: {total_frecuencia}", 0, 1)
        pdf.ln(10)
        
        # Encabezados de tabla
        pdf.set_fill_color(112, 48, 160)  # Púrpura
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", 'B', 12)
        
        # Anchos de columna
        widths = [50, 40, 50]
        headers = ["Emoción", "Frecuencia", "Último Registro"]
        
        for i, header in enumerate(headers):
            pdf.cell(widths[i], 10, header, 1, 0, 'C', True)
        pdf.ln()
        
        # Datos
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", '', 10)
        
        for reporte in datos:
            for i, valor in enumerate(reporte):
                pdf.cell(widths[i], 10, str(valor), 1, 0, 'C')
            pdf.ln()
        
        # Análisis adicional
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "ANÁLISIS EMOCIONAL:", 0, 1)
        pdf.set_font("Arial", '', 10)
        
        if datos:
            emocion_mas_frecuente = max(datos, key=lambda x: int(str(x[1]).split()[0]))
            emocion_menos_frecuente = min(datos, key=lambda x: int(str(x[1]).split()[0]))
            
            pdf.cell(0, 8, f"Emoción más frecuente: {emocion_mas_frecuente[0]} ({emocion_mas_frecuente[1]})", 0, 1)
            pdf.cell(0, 8, f"Emoción menos frecuente: {emocion_menos_frecuente[0]} ({emocion_menos_frecuente[1]})", 0, 1)
        
        # Guardar
        pdf.output(filename)