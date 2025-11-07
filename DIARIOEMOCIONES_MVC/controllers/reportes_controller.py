from models.reporte_model import ReporteModel

class ReporteController:
    def __init__(self, view):
        self.view = view
        self.model = ReporteModel()
    
    def generar_reporte(self, usuario_id, periodo):
        resultados = self.model.generar_reporte_emocional(usuario_id)
        
        if resultados:
            self.view.actualizar_tabla(resultados)
            self.view.mostrar_mensaje("Éxito", f"Reporte generado para usuario {usuario_id}")
        else:
            self.view.mostrar_mensaje("Reporte", "No hay datos para generar el reporte")