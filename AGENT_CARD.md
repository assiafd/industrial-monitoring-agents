# Agent Card

## Projet

Système Intelligent de Surveillance et de Maintenance Industrielle pour une usine automobile.

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
