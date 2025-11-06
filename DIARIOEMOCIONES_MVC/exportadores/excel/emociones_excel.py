import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from datetime import datetime

class EmocionesExcelExporter:
    def exportar(self, emociones, filename=None):
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"reporte_emociones_{timestamp}.xlsx"
        
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Emociones"
        
        # Título
        sheet['A1'] = "CATÁLOGO DE EMOCIONES"
        sheet.merge_cells('A1:C1')
        sheet['A1'].font = Font(bold=True, size=14, color="70AD47")
        sheet['A1'].alignment = Alignment(horizontal="center")
        
        # Encabezados
        headers = ["ID", "Nombre", "Emoji"]
        sheet.append(['', '', ''])
        sheet.append(headers)
        
        # Estilo encabezados
        for cell in sheet[3]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(start_color="70AD47", end_color="70AD47", fill_type="solid")
            cell.alignment = Alignment(horizontal="center")
        
        for emocion in emociones:
            sheet.append(emocion)
        
        # Ajustar columnas
        for column in sheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min((max_length + 2), 50)
            sheet.column_dimensions[column_letter].width = adjusted_width
        
        workbook.save(filename)
        return filename