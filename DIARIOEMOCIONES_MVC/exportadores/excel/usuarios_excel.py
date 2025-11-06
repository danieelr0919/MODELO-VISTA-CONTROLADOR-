import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from datetime import datetime

class UsuariosExcelExporter:
    def exportar(self, usuarios, filename=None):
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"reporte_usuarios_{timestamp}.xlsx"
        
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Usuarios"
        
        # Título
        sheet['A1'] = "REPORTE DE USUARIOS - DIARIO DE EMOCIONES"
        sheet.merge_cells('A1:D1')
        sheet['A1'].font = Font(bold=True, size=14, color="366092")
        sheet['A1'].alignment = Alignment(horizontal="center")
        
        # Encabezados
        headers = ["ID", "Username", "Email", "Fecha Registro"]
        sheet.append(['', '', '', ''])
        sheet.append(headers)
        
        # Estilo encabezados
        self._aplicar_estilo_encabezado(sheet, 3)
        
        # Datos
        for usuario in usuarios:
            sheet.append(usuario)
        
        # Ajustar columnas
        self._ajustar_columnas(sheet)
        
        workbook.save(filename)
        return filename
    
    def _aplicar_estilo_encabezado(self, sheet, fila):
        thin_border = Border(
            left=Side(style='thin'), right=Side(style='thin'),
            top=Side(style='thin'), bottom=Side(style='thin')
        )
        
        for cell in sheet[fila]:
            cell.font = Font(bold=True, color="FFFFFF", size=12)
            cell.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = thin_border
    
    def _ajustar_columnas(self, sheet):
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