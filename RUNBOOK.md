# Runbook Incident

<<<<<<< HEAD
## 1. Vérifier la disponibilité
=======
## Vérifier l'état du service
>>>>>>> c9a031ce3b2c32c38ee1644d82d67990a620e630

```bash
curl http://localhost:8000/health
```

Résultat attendu :

```json
{"status":"ok"}
```

<<<<<<< HEAD
## 2. Reproduire un incident
=======
## Lancer localement

```bash
uvicorn src.main:app --reload
```

Dashboard :

```text
http://localhost:8000
```

## Simuler un incident critique
>>>>>>> c9a031ce3b2c32c38ee1644d82d67990a620e630

```bash
python scripts/simulate_factory.py --critical
```

<<<<<<< HEAD
Ou via Swagger :

```text
http://localhost:8000/docs
```

Utiliser `/analyze` avec une température, vibration ou pression hors seuil.

## 3. Identifier l'exécution

Dans la réponse API, récupérer :

```json
"correlation_id": "..."
```

Ce champ permet de suivre toute l'exécution.

## 4. Lire les événements

Vérifier la liste `events` :

- `monitoring_agent_initialized`
- `receive_telemetry`
- `route_decision`
- `emergency_agent` ou `maintenance_agent`
- `workflow_completed`

## 5. Diagnostic critique

Pour une route critique, vérifier :

- `workflow_status = incident_traced`
- `result.status = critical`
- `result.diagnostic`
- `result.actions`
- `result.agent_prompt`

## 6. Actions d'exploitation

- Notifier l'équipe maintenance.
- Sécuriser la zone.
- Inspecter la machine concernée.
- Conserver le `correlation_id`.
- Ajuster les seuils dans `src/agents/router.py` si les alertes sont trop sensibles.

## 7. Vérifier les tests

```bash
pytest -q
```

Sur GitHub, ouvrir **Actions > CI** et vérifier que le workflow est vert.
=======
## Diagnostic technique

1. Récupérer le `correlation_id` dans la réponse API.
2. Filtrer les logs JSON sur ce `correlation_id`.
3. Vérifier l'étape `route_decision`.
4. Inspecter les anomalies listées dans `details.issues`.
5. Confirmer que `workflow_completed` est présent.

## Actions d'exploitation

- Si `/health` ne répond pas, redémarrer le conteneur ou le service Render.
- Si les tests CI échouent, bloquer le déploiement et corriger avant merge.
- Si trop de faux positifs sont observés, ajuster les seuils dans `Thresholds`.
>>>>>>> c9a031ce3b2c32c38ee1644d82d67990a620e630
