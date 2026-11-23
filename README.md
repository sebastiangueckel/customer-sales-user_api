# Customer & Order API

Das vorliegende Repo ist ein Python-basiertes Backend-Projekt zur Entwicklung und Integration einer REST API basierend auf FastAPI. Das Projekt dient als persönliche Weiterbildung und das Kennenlernen von Schnittstellenentwicklung und verbindet eine lokal ausgeführte PostgreSQL-Datenbank mit einer externen REST API.

Ziel ist es, die Grundlagen einer strukturierten Backend-Architektur praktisch umzusetzen. Das umfasst die Bereitstellung eigener API-Endpunkte über die Datenbankintegration bis hin zum Konsum externer APIs.

## Projektziele

- Entwicklung einer REST API mit FastAPI.
- Bereitstellung von GET- und POST-Endpunkten für Kunden und Aufträge.
- Anbindung einer PostgreSQL-Datenbank.
- Integration einer externen REST API.
- Validierung von Request-Daten und externen API-Antworten mit Pydantic.
- Implementierung einer mehrschichtigen Backend-Architektur.
- Zentrale Fehlerbehandlung und strukturiertes Logging.
- Kennenlernen von Postman als Client zum Testen der definierten Endpunkte

## Tech Stack

| Technologie | Verwendung |
|---|---|
| Python 3.9.5 | Programmiersprache |
| FastAPI | Entwicklung der REST API |
| Uvicorn | ASGI-Server zum Ausführen der Anwendung |
| Pydantic 2.13.5 | Datenmodelle und Validierung |
| PostgreSQL | Relationale Datenbank |
| psycopg2 | Datenbankkommunikation |
| Requests | Kommunikation mit externen REST APIs |
| Postman | Manuelles API-Testing |

### Komponenten

**API Layer – `main.py`**

- Definition der API-Endpunkte und HTTP-Methoden.
- Verarbeitung von Request-Parametern und Request-Bodys.
- Rückgabe der API-Responses.
- Zentrale Registrierung von Exception Handlern.

**Service Layer – `services.py`**

- Implementierung der fachlichen Logik.
- Orchestrierung der benötigten Datenzugriffe.
- Aufruf des Data Access Layers oder des externen API-Clients.
- Verarbeitung und Rückgabe der Ergebnisse.

**Data Access Layer – `data_access.py`**

- Kommunikation mit PostgreSQL.
- Ausführung von SQL-Abfragen.
- Lesen und Schreiben von Daten.
- Verwaltung von Datenbanktransaktionen.

**API Client – `api_client.py`**

- Kommunikation mit externen REST APIs.
- Durchführung von HTTP-Requests mit Requests.
- Konfiguration von Timeouts.
- Verarbeitung und Validierung externer API-Antworten.

**Datenmodelle – `models.py`**

- Definition der Request- und Datenmodelle mit Pydantic.
- Validierung von Datentypen und Datenstrukturen.
- Abbildung verschachtelter Datenobjekte.

**Weitere Konfiguration**

- `database.py`: Aufbau der PostgreSQL-Verbindung.
- `config.py`: Zentrale Konfiguration, beispielsweise die Basis-URL der externen API.
- `logging_config.py`: Konfiguration des Loggings.

## API-Endpunkte

### Kunden

| Methode | Endpunkt | Beschreibung |
|---|---|---|
| GET | `/kunden` | Abruf von Kunden, optional nach Land filterbar |
| POST | `/kunden` | Anlage eines neuen Kunden |

### Aufträge

| Methode | Endpunkt | Beschreibung |
|---|---|---|
| GET | `/auftraege` | Abruf von Aufträgen, optional nach customerkey filterbar |
| POST | `/auftraege` | Anlage eines neuen Auftrags |

### Externe API

| Methode | Endpunkt | Beschreibung |
|---|---|---|
| GET | `/user` | Abruf externer Benutzerdaten über JSONPlaceholder |

Die externe Schnittstelle verwendet:

`https://jsonplaceholder.typicode.com/users`

## Fehlerbehandlung und Logging

Für eine nachvollziehbare Fehlerbehandlung werden zentrale Exception Handler in FastAPI verwendet.

Behandelte Fehlerfälle umfassen unter anderem:

| Fehlerfall | HTTP-Status |
|---|---:|
| Erfolgreicher Abruf | 200 |
| Erfolgreiche Anlage | 201 |
| Datenbank-Fremdschlüsselverletzung | 400 |
| Datenbank-Duplikat / Unique Constraint | 409 |
| Ungültige Request-Daten | 422 |
| Externer HTTP-Fehler | 502 |
| Datenbank- oder Verbindungsfehler | 503 |
| Timeout | 504 |
| Unerwarteter interner Fehler | 500 |

Das Logging erfolgt über das Python-Modul `logging`. Dabei werden beispielsweise API-Aufrufe, Datenbankoperationen und Fehler protokolliert.

## Lokale Installation und Ausführung

### Voraussetzungen

- Python 3.9 oder höher
- PostgreSQL
- Eine lokale Datenbank mit den benötigten Tabellen `customer` und `sales`
- Postman für API-Tests

### 1. Repository vorbereiten

```bash
git clone <REPOSITORY-URL>
cd api-lernen
```

### 2. Virtuelle Umgebung erstellen

Windows / PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Abhängigkeiten installieren

```bash
pip install fastapi uvicorn psycopg2-binary requests pydantic python-dotenv
```

### 4. Konfiguration anpassen

Die Datenbankverbindung wird in `database.py` konfiguriert.

Die Basis-URL der externen API wird in `config.py` hinterlegt.

Datenbankpasswörter und andere Zugangsdaten müssen lokal konfiguriert werden und dürfen nicht im Repository veröffentlicht werden.

### 5. API starten

```bash
python -m uvicorn main:app --reload
```

Die API ist anschließend lokal erreichbar unter:

`http://127.0.0.1:8000`

Die automatisch generierte interaktive API-Dokumentation ist verfügbar unter:

`http://127.0.0.1:8000/docs`

## Testing

Die API-Endpunkte wurden mit Postman getestet.

Dabei wurden unter anderem folgende Szenarien überprüft:

- Erfolgreicher Abruf von Kunden und Aufträgen.
- Filterung von Aufträgen anhand einer Kunden-ID.
- Erfolgreiche Anlage neuer Kunden und Aufträge.
- Behandlung doppelter Datensätze.
- Validierung ungültiger Request-Parameter.
- Aufruf und Validierung einer externen REST API.
- Behandlung von Verbindungsfehlern und Timeouts.

## Lernergebnisse

Im Rahmen dieses Projekts wurden praktische Kenntnisse in folgenden Bereichen aufgebaut:

- REST-API-Design und HTTP-Kommunikation.
- Backend-Entwicklung mit FastAPI.
- Python-Projektstruktur und modularer Aufbau.
- Layered Architecture: API, Service und Data Access Layer.
- Relationale Datenbankintegration mit PostgreSQL und psycopg2.
- Konsum externer REST APIs.
- Datenvalidierung mit Pydantic.
- Fehlerbehandlung und Logging.
- API-Testing mit Postman.

---

*Dieses Projekt ist ein praxisorientiertes Lernprojekt und dient dem Aufbau technischer Kompetenzen in der Entwicklung und Integration von Data- und Backend-Anwendungen.*