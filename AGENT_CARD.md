# Agent Card

## Projet

Système Intelligent de Surveillance et de Maintenance Industrielle pour une usine automobile.

## Agents

| Agent | Responsabilité | Entrées | Sorties |
| --- | --- | --- | --- |
| RouterAgent | Évaluer la télémétrie et choisir la route normale ou critique | Mesures JSON machine | Route, sévérité, anomalies |
| MaintenanceAgent | Traiter le scénario normal et proposer la maintenance préventive | Télémétrie, décision | Diagnostic normal, actions préventives |
| EmergencyAgent | Traiter le scénario critique et produire les actions d'urgence | Télémétrie, décision | Incident, diagnostic, actions sécurité |
| MonitoringAgent | Générer le Correlation ID et tracer chaque étape | Événements workflow | Logs structurés, résumé d'exécution |

## Gouvernance

- Chaque exécution possède un `correlation_id` unique.
- Les décisions de routage sont déterministes et testables.
- Les seuils critiques sont centralisés dans `src/agents/router.py`.
- Les logs sont structurés en JSON pour faciliter l'observabilité.
- Les tests automatisés valident l'aiguillage et l'API.

## Limites

Cette version utilise des règles de seuils explicites. Une évolution possible consiste à brancher un modèle ML ou un LLM dans l'agent d'analyse, en conservant le monitoring et les tests de non-régression.
