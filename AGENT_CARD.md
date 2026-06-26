# Agent Card

## Projet

Système Intelligent de Surveillance et de Maintenance Industrielle pour une usine automobile.

<<<<<<< HEAD
## Objectif

Surveiller une machine industrielle à partir de mesures JSON, détecter les situations critiques, produire un diagnostic et tracer chaque exécution avec un Correlation ID.

## Agents

| Agent | Type | Prompt | Responsabilité |
| --- | --- | --- | --- |
| RouterAgent | Router | `ROUTER_PROMPT` | Analyse la télémétrie et choisit `normal` ou `critical`. |
| MaintenanceAgent | Specialist | `MAINTENANCE_PROMPT` | Produit les recommandations de maintenance préventive. |
| EmergencyAgent | Specialist | `EMERGENCY_PROMPT` | Produit le diagnostic critique et les actions d'urgence. |
| MonitoringAgent | Supervisor | `MONITORING_PROMPT` | Génère le Correlation ID, journalise les étapes et résume l'exécution. |

## État LangGraph

Le state est défini dans `src/state.py` :

- `telemetry`
- `monitoring`
- `decision`
- `result`
- `final_status`
- `response`

## Graphe

Le graphe est défini dans `src/graph.py` :

```text
receive_telemetry
  -> route_machine_state
    -> handle_normal_state
    -> handle_critical_state
  -> finalize_workflow
```

## Gouvernance

- Chaque exécution possède un `correlation_id`.
- Les prompts sont versionnés dans le code source.
- Les seuils de routage sont centralisés dans `Thresholds`.
- Les logs sont structurés en JSON.
- Les tests automatisés valident les routes, l'API, les prompts et l'observabilité.

## Risques et limites

Cette version utilise des prompts déterministes et des règles de seuils. Elle peut être connectée plus tard à un LLM ou à un modèle ML, tout en conservant le même graphe LangGraph et le même state.
=======
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
>>>>>>> c9a031ce3b2c32c38ee1644d82d67990a620e630
