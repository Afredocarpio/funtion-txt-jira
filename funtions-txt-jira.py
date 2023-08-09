import json
import requests
from requests.models import HTTPBasicAuth
from loguru import logger

_CONTENT_TYPE = "application/json"

class CustomizedException(Exception):
    def __init__(self, code_error="ERROR GENERICO", message_error=""):
        self.code_error = code_error
        self.message_error = message_error
        super().__init__(self.code_error, self.message_error)

class JiraHandler:
    def __init__(self, email_user: str, user_token: str, url_jira: str, project_id: str):
        self.email_user = email_user
        self.user_token = user_token
        self.url_jira = url_jira
        self.project_id = project_id

    def get_issue_transitions(self, ticket_id: str) -> dict:
        url = f"{self.url_jira}/rest/api/3/issue/{ticket_id}/transitions"
        response = requests.get(
            url,
            headers={"Accept": _CONTENT_TYPE},
            auth=HTTPBasicAuth(self.email_user, self.user_token),
        )

        if response.status_code != 200:
            raise CustomizedException(
                code_error=f"http_error {response.status_code}",
                message_error="Error al obtener las transiciones del ticket."
            )

        data = response.json()
        transitions_data = [{"id": transition["id"], "name": transition["name"]} for transition in data["transitions"]]

        filename = f"{ticket_id}_transitions.txt"
        with open(filename, "w") as file:
            for transition in transitions_data:
                file.write(json.dumps(transition) + '\n')

        logger.info(f"Transiciones del ticket {ticket_id} guardadas en {filename}")

        return {
            "success": True,
            "message": f"Las transiciones se han guardado en {filename}",
            "filename": filename
        }

if __name__ == "__main__":
    logger.add("app.log", rotation="1 day", level="INFO", format="{time} - {level} - {message}")

    email_user = "###################"   # Reemplaza con tu email
    user_token = "###################"        # Reemplaza con tu token de usuario
    url_jira = "###################" 
    project_id = "###################"         # Reemplaza con tu ID de proyecto

    jira = JiraHandler(email_user, user_token, url_jira, project_id)
    ticket_id = input("Ingrese el ID del ticket: ")
    logger.info(f"Iniciando obtención de transiciones para el ticket {ticket_id}")
    result = jira.get_issue_transitions(ticket_id)
    logger.info(result["message"])
