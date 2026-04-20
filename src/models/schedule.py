class Schedule:
    def __init__(self, id_horario, fecha, hora_inicio, hora_fin, tipo_clase):
        self.id_horario = id_horario
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.tipo_clase = tipo_clase

    def consultar_disponibilidad(self):
        return "Disponible"

    def modificar(self):
        return "Horario modificado"