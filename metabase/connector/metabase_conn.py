import os
import requests
from pprint import pprint
from typing import Any, Dict, List, Union, Optional
import json
from metabase.connector.create_role_and_policy import create_user_with_policy
from psycopg2.errors import DuplicateObject
from django.conf import settings

class MetabaseClient:
    def __init__(self) -> None:
        self.metabase_url = f"{settings.METABASE_URL}/api/"
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self.login()

    def login(self):
        """Logs in and saves the session token."""
        response = self.session.post(
            self.metabase_url + "session",
            json={"username": settings.MB_ADMIN_USER, "password": settings.MB_ADMIN_PASS},
        )
        data = response.json()
        pprint(data)
        self.token = data["id"]
        self.session.headers.update({"X-Metabase-Session": self.token})

    def get_groups_memberships(self):
        """Gets group memberships."""
        response = self.session.get(self.metabase_url + "permissions/group")
        data = response.json()
        return data

    def permissions_graph(self):
        """Gets permissions graph."""
        response = self.session.get(self.metabase_url + "permissions/graph")
        data = response.json()
        return data

    def create_group(self, username):
        """Creates a group."""
        pprint("Creating group")
        response = self.session.post(
            self.metabase_url + "permissions/group",
            json={"name": f"{username}_group"},
        )
        data = response.json()
        return data

    def create_user(self, email: str, fname: str, lname: Optional[str] = None):
        """Creates a metabase user."""
        if lname == "":
            lname = None

        group = self.create_group(fname)
        pprint({"message": "Group created!", "data": group})
        group_id = group["id"]
        response = self.session.post(
            self.metabase_url + "user",
            json={
                "first_name": fname,
                "last_name": lname,
                "email": email,
            },
        )
        user = response.json()
        pprint({"message": "User created!", "data": user})
        user_id = user["id"]

        return user_id, group_id

    def add_user_to_group(self, group_id, user_id):
        """Adds a user to a group."""
        response = self.session.post(
            self.metabase_url + "permissions/membership",
            json={
                "group_id": group_id,
                "user_id": user_id,
            },
        )
        data = response.json()
        return data

    def restringir_acceso_base_datos(
        self, permissions_graph: Dict, database_id: int, user_group: int
    ):
        database_id = str(database_id)  # type: ignore
        group = str(user_group)

        group_ids = list(permissions_graph["groups"].keys())
        group_ids_to_skip = {"2"}
        i = 0
        if group not in group_ids:
            group_ids.append(group)
            permissions_graph["groups"][group] = None

        while i < len(group_ids):
            group_id = group_ids[i]
            if group_id not in group_ids_to_skip:
                group_permissions = permissions_graph["groups"][group_id]
                if (
                    group_permissions is not None
                    and group_permissions.get(database_id)
                    and group_id != group
                ):
                    if group_permissions[database_id].get("data"):
                        data = group_permissions[database_id]["data"]
                        if data.get("native"):
                            data["native"] = "none"
                        if data.get("schemas"):
                            data["schemas"] = "none"
                elif group_id == group:
                    group_permissions = {
                        str(database_id): {
                            "data": {
                                "schemas": "all",
                                "native": "write",
                            }
                        }
                    }
                    permissions_graph["groups"][group_id] = group_permissions
            i += 1
        try:
            response = self.session.put(
                self.metabase_url + "permissions/graph", json=permissions_graph
            )
            response.raise_for_status()
            print("Acceso a la base de datos restringido exitosamente.")
        except requests.exceptions.RequestException as e:
            print("Error al actualizar los permisos de acceso:", str(e))
            raise e
        return permissions_graph

    def obtener_id_database(self, nombre_base_datos):
        url = (
            self.metabase_url + "database"
        )  # Reemplaza <metabase-url> con la URL de tu instancia de Metabase
        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            databases = data["data"]
            for database in databases:
                if database["name"] == nombre_base_datos:
                    return int(database["id"])
            print(
                f"No se encontró la base de datos con el nombre '{nombre_base_datos}'."
            )

        except requests.exceptions.RequestException as e:
            print("Error al obtener la lista de bases de datos:", str(e))
        return None

    def agregar_conexion_metabase(
        self, nombre, tipo_motor, host, puerto, dbname, usuario, password
    ):
        url = self.metabase_url + "database"

        detalles_conexion = {
            "name": nombre,
            "engine": tipo_motor,
            "details": {
                "host": host,
                "port": puerto,
                "dbname": dbname,
                "user": usuario,
                "password": password
                # Otros detalles de conexión según el tipo de base de datos
            },
        }

        headers = {"Content-Type": "application/json"}

        # Realiza la solicitud POST para agregar la conexión a la base de datos
        try:
            response = self.session.post(
                url, headers=headers, data=json.dumps(detalles_conexion)
            )
            response.raise_for_status()  # Verifica si la solicitud fue exitosa
            print("Conexión agregada exitosamente.")
        except requests.exceptions.RequestException as e:
            print("Error al agregar la conexión:", str(e))
