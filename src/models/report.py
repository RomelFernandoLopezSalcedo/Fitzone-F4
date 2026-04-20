class Report:
    def __init__(self, id_reporte, tipo, contenido):
        self.id_reporte = id_reporte
        self.tipo = tipo
        self.contenido = contenido

    def generar(self):
        return "Reporte generado"