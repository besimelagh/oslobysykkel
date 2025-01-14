# Sykkelstasjoner i Oslo

Dette prosjektet viser sanntidsdata for sykkelstasjoner i Oslo på et interaktivt kart.

## Filstruktur
sykkelstasjoner/ ├── backend/ ├── frontend/ ├── docker-compose.yml └── README.md

markdown
Copy code

## Teknologier brukt
- Backend: Flask
- Frontend: Flask + Leaflet.js
- Container: Docker

## Hvordan kjøre prosjektet
1. Installer Docker.
2. Klon dette repoet:
   ```bash
   git clone <repo-url>
   cd sykkelstasjoner
Bygg og start containerne:
bash
Copy code
docker-compose up --build
Åpne nettleseren på http://localhost:5000.


Testing

Backend
Åpne http://localhost:8000/stations i nettleseren for å sjekke JSON-responsen.

Frontend
Åpne http://localhost:5000 og bekreft at kartet vises med markører.

Feilsøking
Sjekk backend-logger ved å åpne terminalen og se etter feil.
Sørg for at Client-Identifier er korrekt i backend/b_app.py.