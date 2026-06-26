# Runbook Incident

## Vérifier l'état du service

```bash
curl http://localhost:8000/health
```

Résultat attendu :

```json
{"status":"ok"}
```

## Lancer localement

```bash
uvicorn src.main:app --reload
```

Dashboard :

```text
http://localhost:8000
```

## Simuler un incident critique

```bash
python scripts/simulate_factory.py --critical
```

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
