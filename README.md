# Minecraft Server Control Panel

Dies ist eine Referenzimplementierung des in `projektbeschreibung.txt` beschriebenen Kontrollpanels.
Sie kombiniert eine FastAPI-gestützte Backend-API, ein minimales PHP-Dashboard sowie
Hilfsskripte für Debian-basierte Systeme.

## Features

- REST-API mit FastAPI und SQLite-Backend
- JWT-Authentifizierung und Benutzerverwaltung (Bootstrap-Endpunkt zum Erstellen eines Admins)
- Verwaltung von Minecraft- und Proxy-Instanzen (Anlegen, Start/Stop/Restart, Einstellungsänderung)
- Beispielhafte Versionsliste für verschiedene Server- und Proxy-Software
- Celery-Worker mit Redis-Anbindung für geplante Aufgaben (Platzhalter)
- PHP-Frontend, das Instanzen per API abruft
- Shell-Skript zur Einrichtung einer virtuellen Umgebung und Konfigurationsdatei

## Systemvoraussetzungen (Debian)

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip redis-server php php-curl sqlite3 openssl
```

## Installation

```bash
git clone <dieses-repo>
cd BlockPilot
./scripts/setup.sh
```

Das Skript legt eine virtuelle Umgebung `.venv` an, installiert alle Python-Abhängigkeiten
und erzeugt eine `.env`-Datei für das Backend.

## Backend starten

```bash
source .venv/bin/activate
cd backend
uvicorn main:app --host 0.0.0.0 --port 8443
```

### Admin-Benutzer anlegen

```bash
http POST http://localhost:8443/api/v1/auth/bootstrap username=admin password=geheimespasswort
```

Alternativ kann `curl` verwendet werden.

### Anmelden und Token nutzen

```bash
http --form POST http://localhost:8443/api/v1/auth/login username=admin password=geheimespasswort
```

Das erhaltene `access_token` als `Authorization: Bearer <token>` in weiteren API-Aufrufen mitsenden.

## Celery-Worker

```bash
source .venv/bin/activate
cd backend
celery -A app.tasks worker -l info
```

## PHP-Dashboard

Einen einfachen PHP-Server im Verzeichnis `web/` starten:

```bash
php -S 0.0.0.0:8000 -t web
```

Standardmäßig greift das Dashboard auf `http://localhost:8443/api/v1/instances` zu. Der API-Basis-URL kann
über die Umgebungsvariable `API_BASE` angepasst werden.

## Verzeichnisstruktur

```
backend/
  app/
    auth.py
    config.py
    database.py
    models.py
    routers/
    schemas.py
    services/
    tasks.py
  celery_worker.py
  main.py
scripts/
  setup.sh
web/
  index.php
```

## Tests

Für einen Syntax-Check kann `python -m compileall backend` ausgeführt werden.
