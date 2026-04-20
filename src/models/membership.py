class Membership:
    def __init__(self, id_membresia, tipo, fecha_inicio, fecha_fin, estado):
        self.id_membresia = id_membresia
        self.tipo = tipo
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado

    def seleccionar(self):
        return "Membresía seleccionada"

    def actualizar_estado(self):
        return "Estado actualizado"