# Industrial Monitoring Agents

<<<<<<< HEAD
Projet : **Système Intelligent de Surveillance et de Maintenance Industrielle** pour le secteur automobile.

L'application expose une API FastAPI et un dashboard minimaliste. Elle reçoit une télémétrie machine au format JSON, exécute un workflow multi-agents avec **LangGraph** et retourne une décision `normal` ou `critical` avec un diagnostic, un `correlation_id` et les événements d'observabilité.

## Respect de l'énoncé

- Architecture multi-agents spécialisée automobile.
- Agents basés sur des prompts dans `src/prompts.py`.
- Orchestration avec `LangGraph` dans `src/graph.py`.
- État partagé du workflow dans `src/state.py`.
- Agent de monitoring avec `correlation_id` et logs structurés.
- Tests automatisés avec `pytest` et GitHub Actions.
- Conteneurisation avec Docker.
- API déployable sur Render.
- Documentation technique, Agent Card et Runbook incident.
=======
Système intelligent de surveillance et de maintenance industrielle pour le secteur automobile. L'application reçoit des données de télémétrie machine, analyse l'état de santé de l'équipement, route le workflow vers un scénario normal ou critique et journalise chaque étape avec un Correlation ID.
>>>>>>> c9a031ce3b2c32c38ee1644d82d67990a620e630

## Architecture

```text
<<<<<<< HEAD
Télémétrie JSON
      |
      v
FastAPI /analyze
      |
      v
LangGraph StateGraph
      |
      +--> MonitoringAgent: Correlation ID, logs, durée
      |
      +--> RouterAgent: prompt + décision normal/critical
               |
               +--> MaintenanceAgent: prompt + actions préventives
               |
               +--> EmergencyAgent: prompt + diagnostic incident
```

## Fichiers importants

```text
src/main.py                  API FastAPI et dashboard
src/graph.py                 Graphe LangGraph
src/state.py                 State partagé du workflow
src/prompts.py               Prompts des agents
src/agents/router.py         Agent de routage normal/critical
src/agents/maintenance.py    Agent de maintenance préventive
src/agents/emergency.py      Agent d'urgence
src/agents/monitoring.py     Agent monitoring et Correlation ID
tests/                       Tests automatisés
.github/workflows/main.yml   CI GitHub Actions
Dockerfile                   Conteneurisation
AGENT_CARD.md                Gouvernance des agents
RUNBOOK.md                   Gestion d'incident
```

## Installation locale

Utiliser Python 3.11.
=======
Simulateur JSON -> API FastAPI -> RouterAgent -> MaintenanceAgent ou EmergencyAgent
                                      |
                                      v
                               MonitoringAgent
```

## Installation
>>>>>>> c9a031ce3b2c32c38ee1644d82d67990a620e630

```bash
python -m venv .venv
.venv\Scripts\activate
<<<<<<< HEAD
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

## Lancer l'application
=======
pip install -r requirements.txt
```

## Lancement
>>>>>>> c9a031ce3b2c32c38ee1644d82d67990a620e630

```bash
uvicorn src.main:app --reload
```

<<<<<<< HEAD
Ouvrir :
=======
Ouvrir le dashboard :
>>>>>>> c9a031ce3b2c32c38ee1644d82d67990a620e630

```text
http://localhost:8000
```

<<<<<<< HEAD
Documentation API :

```text
http://localhost:8000/docs
```

## Exemple de test API
=======
## Exemple API
>>>>>>> c9a031ce3b2c32c38ee1644d82d67990a620e630

```bash
curl -X POST http://localhost:8000/analyze ^
  -H "Content-Type: application/json" ^
  -d "{\"machine_id\":\"ROBOT-SOUDURE-01\",\"temperature_c\":92,\"vibration_mm_s\":8.4,\"pressure_bar\":10.5,\"energy_kw\":39,\"rotation_rpm\":1800,\"error_code\":\"E_TEMP\"}"
```

<<<<<<< HEAD
La réponse contient :

- `correlation_id`
- `workflow_status`
- `events`
- `result.status`
- `result.agent_prompt`
- `result.diagnostic`
- `result.actions`

## Simulation usine

Télémétrie normale :

```bash
python scripts/simulate_factory.py
```

Télémétrie critique :

```bash
=======
## Simulation

```bash
python scripts/simulate_factory.py
>>>>>>> c9a031ce3b2c32c38ee1644d82d67990a620e630
python scripts/simulate_factory.py --critical
```

## Tests

```bash
pytest -q
```

<<<<<<< HEAD
Les tests vérifient :

- route normale ;
- route critique ;
- présence des prompts ;
- présence du `correlation_id` ;
- fonctionnement de l'API.

## GitHub Actions

Le workflow `.github/workflows/main.yml` lance automatiquement :

```bash
pytest -q
```

Après chaque `push`, ouvrir l'onglet **Actions** du repository GitHub et vérifier que le workflow **CI** est vert.

=======
>>>>>>> c9a031ce3b2c32c38ee1644d82d67990a620e630
## Docker

```bash
docker build -t industrial-monitoring-agents .
docker run -p 8000:8000 industrial-monitoring-agents
```

## Déploiement Render

<<<<<<< HEAD
Créer un nouveau **Web Service** Render depuis le repository GitHub, choisir Docker, puis déployer. Le `Dockerfile` lance automatiquement :
=======
Utiliser le `Dockerfile` fourni. La commande de démarrage est déjà définie :
>>>>>>> c9a031ce3b2c32c38ee1644d82d67990a620e630

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## Démo vidéo

<<<<<<< HEAD
Lien à ajouter après enregistrement : `https://example.com/demo-video`
=======
Lien à ajouter : `https://example.com/demo-video`
>>>>>>> c9a031ce3b2c32c38ee1644d82d67990a620e630
