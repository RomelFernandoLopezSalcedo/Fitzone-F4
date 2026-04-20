class Notification:
    def __init__(self, id_notificacion, tipo, mensaje):
        self.id_notificacion = id_notificacion
        self.tipo = tipo
        self.mensaje = mensaje

    def enviar_cliente(self):
        return f"Notificación al cliente: {self.mensaje}"

    def enviar_trabajador(self):
        return f"Notificación al trabajador: {self.mensaje}"