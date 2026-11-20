from data_access import (
    kunden_abrufen,
    kunden_anlegen,
    auftraege_abrufen,
    auftrag_anlegen)
import logging
from api_client import benutzer_abrufen

logger = logging.getLogger(__name__)
def kunden_abrufen_service(country=None):
    logger.info("Kundenabfrage gestartet")
    kunden = kunden_abrufen(country)
    logger.info("%s Kunden abgerufen", len(kunden))
    return kunden

def kunden_anlegen_service(kunde):
    logger.info(
        "Kundenanlage gestartet: CustomerKey %s",
        kunde.customerkey
    )
    neuer_kunde = kunden_anlegen(kunde)
    logger.info(
        "Kunde erfolgreich angelegt: CustomerKey %s",
        kunde.customerkey
    )
    return neuer_kunde

def auftraege_abrufen_service(kunde=None):
    logger.info("Auftragsabfrage gestartet")
    auftraege = auftraege_abrufen(kunde)
    logger.info("%s Aufträge abgerufen", len(auftraege))
    return auftraege

def auftraege_anlegen_service(auftrag):
    logger.info(
        "Auftragsanlage gestartet: orderkey %s",
        auftrag.orderkey
    )
    neuer_auftrag = auftrag_anlegen(auftrag)
    logger.info(
        "Auftrag erfolgreich angelegt: orderkey %s",
        auftrag.orderkey
    )
    return neuer_auftrag

def externe_benutzer_abrufen_service():
    logger.info("Externe Benutzerabfrage gestartet")
    externe_benutzer = benutzer_abrufen()
    logger.info("Externe Benutzerabfrage erfolgreich")
    return externe_benutzer


