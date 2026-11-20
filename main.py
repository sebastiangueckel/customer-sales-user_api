from typing import Optional
from fastapi import FastAPI, Request
import psycopg2
import requests
from services import (
    kunden_abrufen_service,
    kunden_anlegen_service,
    auftraege_abrufen_service,
    auftraege_anlegen_service,
    externe_benutzer_abrufen_service)
from logging_config import setup_logging
import logging
from fastapi.responses import JSONResponse
from models import CustomerCreate, AuftragCreate
import pydantic_core

setup_logging()
logger = logging.getLogger(__name__)
logger.info("Anwendung wird gestartet")

app = FastAPI()

@app.exception_handler(psycopg2.OperationalError)
async def database_exception_handler(request: Request, exc: psycopg2.OperationalError):
    logger.exception("Datenbankfehler aufgetreten")
    return JSONResponse(
        status_code=503,
        content={
            "detail": "Datenbank aktuell nicht verfügbar."
        }
    )

@app.exception_handler(psycopg2.errors.UniqueViolation)
async def database_exception_handler(request: Request, exc: psycopg2.errors.UniqueViolation):
    logger.warning("Unique Constraint verletzt: %s", exc.diag.constraint_name)
    return JSONResponse(
        status_code=409,
        content={
            "detail": "Bereits angelegter Datensatz kann nicht doppelt anlegt werden."
        }
    )

@app.exception_handler(psycopg2.errors.ForeignKeyViolation)
async def database_exception_handler(request: Request, exc: psycopg2.errors.ForeignKeyViolation):
    logger.warning("Fremdschlüssel nicht vorhanden.")
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Der hinterlegte Fremdschlüssel existiert nicht."
        }
    )

@app.exception_handler(requests.exceptions.Timeout)
async def api_timeout_handler(request, exc: requests.exceptions.Timeout):
    logger.exception("Der Server ist in ein Timeout gelaufen.")
    return JSONResponse(
        status_code=504,
        content={
            "detail": "Die Abfrage dauert zu lange - Timeout."
        }
    )

@app.exception_handler(requests.exceptions.ConnectionError)
async def api_connection_handler(request, exc: requests.exceptions.ConnectionError):
    logger.exception("Verbindung zum externen API-Dienst fehlgeschlagen")
    return JSONResponse(
        status_code=503,
        content={
            "detail": "Der externe Dienst ist aktuell nicht erreichbar."
        }
    )

@app.exception_handler(requests.exceptions.HTTPError)
async def api_httperror_handler(request, exc: requests.exceptions.HTTPError):
    logger.exception("Fehlerhafte HTTP-Antwort des externen API-Dienstes")
    return JSONResponse(
        status_code=502,
        content={
            "detail": "Der externe Dienst hat eine fehlerhafte Antwort geliefert."
        }
    )

@app.exception_handler(pydantic_core._pydantic_core.ValidationError)
async def api_ValidatonError(request, exc: pydantic_core._pydantic_core.ValidationError):
    logger.exception("Unerwartete Antwort vom Backend erhalten.")
    return JSONResponse(
        status_code=502,
        content={
            "detail": "Es wurde eine unerwartete Antwort vom Backend zurückgegeben."
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.exception("Unerwarteter Fehler aufgetreten")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Ein interner Serverfehler ist aufgetreten."
        }
    )

@app.get("/kunden")
def get_kunden(country: Optional[str] = None):
    kunden = kunden_abrufen_service(country)
    return kunden

@app.post("/kunden", status_code=201)
def post_kunde(kunde: CustomerCreate):
    neuer_kunde = kunden_anlegen_service(kunde)
    return neuer_kunde

@app.get("/auftraege")
def get_auftraege(kunde: Optional[int] = None):
    auftraege = auftraege_abrufen_service(kunde)
    return auftraege

@app.post("/auftraege", status_code=201)
def post_auftrag(auftrag: AuftragCreate):
    neuer_auftrag = auftraege_anlegen_service(auftrag)
    return neuer_auftrag

@app.get("/user")
def get_externe_benutzer():
    externe_benutzer = externe_benutzer_abrufen_service()
    return externe_benutzer