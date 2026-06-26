# Runbook Incident

## 1. Vérifier la disponibilité

```bash
curl http://localhost:8000/health
```

Résultat attendu :

```json
{"status":"ok"}
```

## 2. Reproduire un incident

```bash
python scripts/simulate_factory.py --critical
```

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
