class Worker:
    def __init__(self, id_trabajador, nombre, cargo, telefono, correo, estado_laboral):
        self.id_trabajador = id_trabajador
        self.nombre = nombre
        self.cargo = cargo
        self.telefono = telefono
        self.correo = correo
        self.estado_laboral = estado_laboral

    def registrar(self):
        return "Trabajador registrado"

    def actualizar_datos(self):
        return "Datos actualizados"