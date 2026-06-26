# Projet : Système Intelligent de Surveillance et de Maintenance Industrielle

## Version

Version actuelle : `1.1.0`

Cette version ajoute l’envoi automatique d’un rapport d’incident vers Slack lorsqu’une machine passe au statut critique.

## 1. Présentation

Ce projet met en œuvre une architecture multi-agents pour la surveillance intelligente d’une machine industrielle dans le secteur automobile.

L’application reçoit des données de télémétrie machine au format JSON, analyse l’état de l’équipement avec un workflow orchestré par LangGraph, puis affiche les résultats dans un dashboard de supervision dynamique.

Le système permet de :

- détecter automatiquement les situations normales ou critiques ;
- produire un diagnostic synthétique ;
- proposer des actions de maintenance préventive ou d’urgence ;
- tracer chaque exécution avec un Correlation ID ;
- visualiser les mesures sous forme de graphiques ;
- tester le projet automatiquement avec GitHub Actions ;
- conteneuriser et déployer l’application avec Docker et Render.

## 2. Objectif du projet

L’objectif est de répondre à un besoin industriel courant : surveiller en continu des machines de production automobile comme des robots de soudure, convoyeurs, presses hydrauliques ou machines CNC.

Une machine envoie des mesures telles que :

- température ;
- vibrations ;
- pression ;
- consommation énergétique ;
- vitesse de rotation ;
- code erreur.

Le système analyse ces données et décide automatiquement si la machine fonctionne normalement ou si une intervention est nécessaire.

## 3. Architecture générale

```text
Machine industrielle ou simulateur
        |
        v
POST /telemetry
        |
        v
API FastAPI
        |
        v
Workflow LangGraph
        |
        +--> MonitoringAgent
        |       - Correlation ID
        |       - logs
        |       - durée d’exécution
        |
        +--> RouterAgent
                - analyse des seuils
                - route normal / critical
                |
                +--> MaintenanceAgent
                |       - diagnostic normal
                |       - maintenance préventive
                |
                +--> EmergencyAgent
                        - diagnostic critique
                        - actions d’urgence
        |
        v
GET /telemetry/latest
        |
        v
Dashboard dynamique
```

## 4. Technologies utilisées

| Technologie | Rôle |
| --- | --- |
| Python 3.11 | Langage principal |
| FastAPI | API backend et documentation Swagger |
| LangGraph | Orchestration du workflow multi-agents |
| Pydantic | Validation des données de télémétrie |
| Jinja2 | Rendu du dashboard HTML |
| Tailwind CSS | Design du dashboard |
| Chart.js | Graphiques de télémétrie |
| Pytest | Tests automatisés |
| GitHub Actions | Intégration continue |
| Docker | Conteneurisation |
| Render | Déploiement cloud |
| Slack API | Notification des incidents critiques |

## 5. Structure du projet

```text
industrial-monitoring-agents/
│
├── .github/
│   └── workflows/
│       └── main.yml
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── graph.py
│   ├── state.py
│   ├── prompts.py
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── maintenance.py
│   │   ├── emergency.py
│   │   └── monitoring.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── utils/
│       └── logger.py
│
├── tests/
│   ├── __init__.py
│   ├── test_router.py
│   └── test_api.py
│
├── scripts/
│   └── simulate_factory.py
│
├── .env.example
├── .gitignore
├── AGENT_CARD.md
├── RUNBOOK.md
├── Dockerfile
├── README.md
└── requirements.txt
```

## 6. Agents du système

### 6.1 MonitoringAgent

Le `MonitoringAgent` est responsable de l’observabilité du workflow.

Il permet de :

- générer un Correlation ID unique ;
- enregistrer chaque étape du workflow ;
- conserver les horodatages ;
- calculer la durée d’exécution ;
- produire un résumé final.

Chaque réponse contient un champ :

```json
"correlation_id": "..."
```

Ce champ permet de suivre une exécution complète du système.

### 6.2 RouterAgent

Le `RouterAgent` analyse les mesures reçues et décide de la route à suivre.

Il vérifie notamment :

- température supérieure au seuil ;
- vibrations anormales ;
- pression élevée ;
- consommation électrique élevée ;
- vitesse de rotation hors plage ;
- code erreur machine.

Routes possibles :

```text
normal
critical
```

### 6.3 MaintenanceAgent

Le `MaintenanceAgent` traite les cas normaux.

Il produit :

- un diagnostic de bon fonctionnement ;
- des actions de surveillance ;
- des recommandations de maintenance préventive.

### 6.4 EmergencyAgent

Le `EmergencyAgent` traite les situations critiques.

Il produit :

- un diagnostic d’incident ;
- une synthèse des anomalies ;
- des actions immédiates ;
- des recommandations liées au runbook incident.

## 7. Prompts des agents

Les prompts sont centralisés dans :

```text
src/prompts.py
```

Le projet contient un prompt pour chaque agent :

- `ROUTER_PROMPT`
- `MAINTENANCE_PROMPT`
- `EMERGENCY_PROMPT`
- `MONITORING_PROMPT`

Ces prompts décrivent clairement le rôle de chaque agent et rendent l’architecture plus proche d’un système agentique.

## 8. Workflow LangGraph

Le graphe est défini dans :

```text
src/graph.py
```

Flux d’exécution :

```text
receive_telemetry
  -> route_machine_state
    -> handle_normal_state
    -> handle_critical_state
  -> finalize_workflow
```

Le state partagé est défini dans :

```text
src/state.py
```

Il contient :

- `telemetry`
- `monitoring`
- `decision`
- `result`
- `final_status`
- `response`

## 9. API FastAPI

L’API est définie dans :

```text
src/main.py
```

### 9.1 Routes disponibles

| Méthode | Route | Description |
| --- | --- | --- |
| GET | `/` | Dashboard de supervision |
| GET | `/health` | Vérification de disponibilité |
| POST | `/analyze` | Analyse directe d’une télémétrie |
| POST | `/telemetry` | Réception des données machine |
| GET | `/telemetry/latest` | Dernière télémétrie analysée |
| GET | `/telemetry/history` | Historique récent des télémétries |

### 9.2 Format d’entrée

```json
{
  "machine_id": "ROBOT-SOUDURE-01",
  "temperature_c": 96,
  "vibration_mm_s": 9.1,
  "pressure_bar": 13,
  "energy_kw": 48,
  "rotation_rpm": 3800,
  "error_code": "E_TEMP"
}
```

### 9.3 Format de sortie

La réponse contient notamment :

- `correlation_id`
- `workflow_status`
- `events`
- `duration_ms`
- `result.status`
- `result.diagnostic`
- `result.actions`
- `result.agent_prompt`

## 10. Dashboard de supervision

Le dashboard est disponible à l’adresse :

```text
http://localhost:8000
```

Il affiche :

- l’état de la machine ;
- la sévérité ;
- la durée du workflow ;
- l’identifiant machine ;
- le Correlation ID ;
- les graphiques de télémétrie ;
- le score de risque ;
- la timeline LangGraph ;
- les actions recommandées.

### 10.1 Supervision active

Le bouton ON/OFF permet d’activer ou de mettre en pause la supervision automatique.

Quand la supervision est active, le dashboard interroge :

```text
GET /telemetry/latest
```

### 10.2 Fréquence de rafraîchissement

La fréquence actuelle est définie dans :

```text
src/templates/index.html
```

Variable :

```js
const refreshIntervalMs = 2500;
```

`2500` correspond à 2,5 secondes.

### 10.3 Acquittement d’alerte

Le bouton **Acquitter alerte** apparaît uniquement lorsque l’état machine est critique.

Il permet à l’opérateur de signaler que l’alerte a été prise en compte.

### 10.4 Export du rapport

Le bouton **Exporter rapport** génère un fichier texte contenant :

- machine ;
- statut ;
- sévérité ;
- Correlation ID ;
- télémétrie ;
- diagnostic ;
- actions recommandées.

## 11. Simulateur de machine

Le simulateur est défini dans :

```text
scripts/simulate_factory.py
```

Il envoie des données vers :

```text
POST /telemetry
```

### 11.1 Simulation normale

```bash
python scripts/simulate_factory.py --loop
```

### 11.2 Simulation critique

```bash
python scripts/simulate_factory.py --critical --loop
```

### 11.3 Modifier l’intervalle

```bash
python scripts/simulate_factory.py --loop --interval 5
```

Cette commande envoie une télémétrie toutes les 5 secondes.

## 12. Installation locale

### 12.1 Prérequis

Utiliser Python 3.11.

Vérifier la version :

```bash
python --version
```

### 12.2 Créer un environnement virtuel

```bash
py -3.11 -m venv .venv
.venv\Scripts\activate
```

### 12.3 Installer les dépendances

```bash
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

## 13. Lancement local

```bash
uvicorn src.main:app --reload
```

Ouvrir ensuite :

```text
http://localhost:8000
```

Documentation Swagger :

```text
http://localhost:8000/docs
```

## 14. Tests automatisés

Lancer les tests :

```bash
pytest -q
```

Les tests vérifient :

- la route normale ;
- la route critique ;
- la présence des prompts ;
- la présence du Correlation ID ;
- le fonctionnement de l’API.

## 15. GitHub Actions

Le workflow CI se trouve ici :

```text
.github/workflows/main.yml
```

Il s’exécute automatiquement à chaque push sur la branche `main`.

Commande exécutée :

```bash
pytest -q
```

Le fichier configure aussi :

```yaml
PYTHONPATH: .
```

afin que les imports `src.*` fonctionnent correctement dans GitHub Actions.

## 16. Docker

### 16.1 Construire l’image

```bash
docker build -t industrial-monitoring-agents .
```

### 16.2 Lancer le conteneur

```bash
docker run -p 8000:8000 industrial-monitoring-agents
```

Ouvrir :

```text
http://localhost:8000
```

## 17. Déploiement Render

Étapes :

1. Aller sur Render.
2. Créer un nouveau **Web Service**.
3. Connecter le repository GitHub.
4. Choisir l’environnement Docker.
5. Déployer le service.

Le `Dockerfile` lance automatiquement :

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

Une fois déployé, l’application est accessible via l’URL Render.

## 18. Runbook incident

Le guide d’incident est disponible dans :

```text
RUNBOOK.md
```

Il explique comment :

- vérifier l’état du service ;
- reproduire un incident ;
- récupérer le Correlation ID ;
- lire les événements ;
- analyser un diagnostic critique ;
- vérifier les tests.

## 19. Notification Slack des incidents critiques

Quand une machine passe au statut `critical`, l’`EmergencyAgent` prépare un rapport d’incident et tente de l’envoyer vers Slack.

Le message Slack contient :

- machine concernée ;
- Correlation ID ;
- diagnostic ;
- principales mesures de télémétrie ;
- actions recommandées.

### 19.1 Variables d’environnement

Créer un fichier `.env` local ou configurer les variables dans Render :

```env
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_CHANNEL_NAME=nouveau-canal
```

Ne jamais pousser le fichier `.env` sur GitHub.

### 19.2 Scopes Slack nécessaires

Le bot Slack doit avoir au minimum :

```text
chat:write
channels:read
groups:read
```

Le bot doit aussi être ajouté au canal Slack cible.

### 19.3 Comportement sans token

Si `SLACK_BOT_TOKEN` n’est pas configuré, l’envoi Slack est ignoré proprement :

```json
{
  "status": "skipped",
  "reason": "SLACK_BOT_TOKEN is not configured"
}
```

Cela permet aux tests automatisés et à GitHub Actions de fonctionner sans secret.

## 20. Gouvernance des agents

La gouvernance est documentée dans :

```text
AGENT_CARD.md
```

Ce fichier décrit :

- les agents ;
- leurs responsabilités ;
- leurs entrées ;
- leurs sorties ;
- le state LangGraph ;
- les règles de traçabilité ;
- les limites du système.

## 21. Scénario de démonstration

### 21.1 Lancer l’application

```bash
uvicorn src.main:app --reload
```

### 21.2 Ouvrir le dashboard

```text
http://localhost:8000
```

### 21.3 Lancer le simulateur normal

```bash
python scripts/simulate_factory.py --loop
```

Le dashboard affiche un état normal.

### 21.4 Lancer le simulateur critique

```bash
python scripts/simulate_factory.py --critical --loop
```

Le dashboard affiche :

- état critique ;
- sévérité élevée ;
- diagnostic d’incident ;
- actions recommandées ;
- bouton d’acquittement d’alerte.

Si Slack est configuré, un rapport d’incident est envoyé automatiquement dans le canal défini par `SLACK_CHANNEL_NAME`.

### 21.5 Exporter un rapport

Cliquer sur :

```text
Exporter rapport
```

Le rapport généré contient les informations nécessaires au suivi de l’incident.

## 22. Critères de validation couverts

| Critère | Statut |
| --- | --- |
| Architecture multi-agents | Couvert |
| Agent de monitoring | Couvert |
| Correlation ID | Couvert |
| Prompts agents | Couvert |
| LangGraph + State | Couvert |
| Tests automatisés | Couvert |
| GitHub Actions | Couvert |
| Docker | Couvert |
| Déploiement Render | Couvert |
| Runbook incident | Couvert |
| Agent Card | Couvert |
| Dashboard dynamique | Couvert |
| Documentation technique | Couvert |
| Notification Slack en cas critique | Couvert |

## 23. Conclusion

Ce projet fournit une solution complète de surveillance industrielle intelligente. Il combine une architecture multi-agents, un workflow LangGraph, un agent de monitoring, une API FastAPI, un dashboard dynamique, des tests automatisés, Docker et un déploiement cloud.

La solution permet de détecter rapidement les anomalies machine, de produire un diagnostic exploitable et d’assurer une traçabilité complète de chaque exécution.
