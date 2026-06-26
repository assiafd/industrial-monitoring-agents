# Industrial Monitoring Agents

Système intelligent de surveillance et de maintenance industrielle pour le secteur automobile. L'application reçoit des données de télémétrie machine, analyse l'état de santé de l'équipement, route le workflow vers un scénario normal ou critique et journalise chaque étape avec un Correlation ID.

## Architecture

```text
Simulateur JSON -> API FastAPI -> RouterAgent -> MaintenanceAgent ou EmergencyAgent
                                      |
                                      v
                               MonitoringAgent
```

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Lancement

```bash
uvicorn src.main:app --reload
```

Ouvrir le dashboard :

```text
http://localhost:8000
```

## Exemple API

```bash
curl -X POST http://localhost:8000/analyze ^
  -H "Content-Type: application/json" ^
  -d "{\"machine_id\":\"ROBOT-SOUDURE-01\",\"temperature_c\":92,\"vibration_mm_s\":8.4,\"pressure_bar\":10.5,\"energy_kw\":39,\"rotation_rpm\":1800,\"error_code\":\"E_TEMP\"}"
```

## Simulation

```bash
python scripts/simulate_factory.py
python scripts/simulate_factory.py --critical
```

## Tests

```bash
pytest -q
```

## Docker

```bash
docker build -t industrial-monitoring-agents .
docker run -p 8000:8000 industrial-monitoring-agents
```

## Déploiement Render

Utiliser le `Dockerfile` fourni. La commande de démarrage est déjà définie :

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## Démo vidéo

Lien à ajouter : `https://example.com/demo-video`
