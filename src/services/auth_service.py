import json
import os
from datetime import datetime
from src.models.client import Client


class AuthService:
    def __init__(self):
        self.users = []
        self.logs = []

        self.user_file = "data/users.json"
        self.log_file = "data/logs.json"

        self.id_counter = 1

        self.load_users()
        self.load_logs()

    # 🟩 LOGS
    def add_log(self, message):
        log = {
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "message": message
        }

        self.logs.append(log)
        self.save_logs()

    # 🟩 CARGAR LOGS
    def load_logs(self):
        if not os.path.exists("data"):
            os.makedirs("data")

        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as file:
                self.logs = json.load(file)
        else:
            self.logs = []

    # 🟩 GUARDAR LOGS
    def save_logs(self):
        with open(self.log_file, "w") as file:
            json.dump(self.logs, file, indent=4)

    # 🟩 USUARIOS
    def load_users(self):
        if not os.path.exists("data"):
            os.makedirs("data")

        if os.path.exists(self.user_file):
            with open(self.user_file, "r") as file:
                data = json.load(file)

                for u in data:
                    user = Client(
                        u["id"],
                        u["name"],
                        u["email"],
                        u["password"],
                        u["role"]
                    )

                    user.payments = u.get("payments", [])
                    user.membership = u.get("membership", None)

                    self.users.append(user)

                    if u["id"] >= self.id_counter:
                        self.id_counter = u["id"] + 1
        else:
            # usuarios iniciales
            self.create_user("Romel", "admin@mail.com", "1234", "admin")
            self.create_user("Juan", "user@mail.com", "1234", "user")
            self.create_user("Seguridad", "seg@mail.com", "1234", "seguridad")

    def save_users(self):
        data = []

        for user in self.users:
            data.append({
                "id": user.id_cliente,
                "name": user.nombre,
                "email": user.correo,
                "password": user.password,
                "role": user.role,
                "payments": user.payments,
                "membership": user.membership
            })

        with open(self.user_file, "w") as file:
            json.dump(data, file, indent=4)

    # 🟩 CREATE
    def create_user(self, name, email, password, role):
        user = Client(self.id_counter, name, email, password, role)
        self.users.append(user)
        self.id_counter += 1

        self.add_log(f"Usuario creado: {name}")
        self.save_users()

        return user

    # 🟩 READ
    def get_users(self):
        return self.users

    # 🟩 UPDATE
    def update_user(self, email, new_name):
        for user in self.users:
            if user.get_email() == email:
                user.nombre = new_name
                self.add_log(f"Usuario actualizado: {email}")
                self.save_users()
                return True
        return False

    # 🟩 DELETE
    def delete_user(self, email):
        for user in self.users:
            if user.get_email() == email:
                self.users.remove(user)
                self.add_log(f"Usuario eliminado: {email}")
                self.save_users()
                return True
        return False

    # 🟩 LOGIN
    def login(self, email, password):
        for user in self.users:
            if user.get_email() == email and user.password == password:
                self.add_log(f"{user.get_name()} inició sesión")
                return user

        self.add_log(f"Intento fallido de login: {email}")
        return None

    # 🟩 PAGOS
    def add_payment(self, email, value, method):
        for user in self.users:
            if user.get_email() == email:
                user.payments.append({
                    "value": value,
                    "method": method
                })

                self.add_log(f"Pago registrado para {email}")
                self.save_users()
                return True
        return False

    # 🟩 NOTIFICACIÓN
    def send_notification(self, message):
        self.add_log(f"Notificación enviada: {message}")
        print(f"NOTIFICACIÓN: {message}")
