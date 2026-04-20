from src.models.worker import Worker

class Trainer(Worker):
    def __init__(self, id_trabajador, nombre, especialidad, disponibilidad):
        super().__init__(id_trabajador, nombre, "Entrenador", "", "", "")
        self.especialidad = especialidad
        self.disponibilidad = disponibilidad

    def evaluar_desempeno(self):
        return "Desempeño evaluado"

    def asignar_horario(self):
        return "Horario asignado"