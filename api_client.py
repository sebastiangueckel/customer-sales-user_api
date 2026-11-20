import requests
import logging
from config import JSONPLACEHOLDER_BASE_URL
from models import ExternalBenutzer

logger = logging.getLogger(__name__)

def benutzer_abrufen():
    endpoint = f"{JSONPLACEHOLDER_BASE_URL}/users"
    logger.info("Starte API-Abfrage für Kunden")
    response = requests.get(endpoint, timeout= (3, 10))
    response.raise_for_status()
    benutzer = response.json()
    validierte_benutzer =[]
    for user in benutzer:
        validiert = ExternalBenutzer.model_validate(user)
        validierte_benutzer.append(validiert)
    anzahl_benutzer = len(benutzer)
    logger.info("API-Abfrage erfolgreich: %s Datensätze", anzahl_benutzer)
    return validierte_benutzer