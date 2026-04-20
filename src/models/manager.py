from src.models.worker import Worker

class Manager(Worker):
    def __init__(self, id_trabajador, nombre):
        super().__init__(id_trabajador, nombre, "Gerente", "", "", "")

    def administrar_horarios(self):
        return "Horarios administrados"

    def administrar_tarifas(self):
        return "Tarifas administradas"

    def generar_reportes(self):
        return "Reporte generado"