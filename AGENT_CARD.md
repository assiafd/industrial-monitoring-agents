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

## Modèle LLM

Les agents `RouterAgent`, `MaintenanceAgent`, `EmergencyAgent` et `MonitoringAgent` utilisent Google Gemini 2.5 Flash lorsque la variable `GOOGLE_API_KEY` est configurée.

Configuration :

```text
GOOGLE_API_KEY=your_google_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

Si la clé API n'est pas configurée, le workflow continue avec la logique déterministe de seuils et le bloc `llm.response.status` indique `skipped`. Pour `MonitoringAgent`, les logs techniques restent déterministes ; Gemini sert uniquement à générer un résumé lisible dans `monitoring_summary`.

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
- Les tests automatisés valident les routes, l'API, les prompts, le fallback LLM et l'observabilité.

## Risques et limites

La décision critique reste sécurisée par des règles de seuils. Gemini enrichit le raisonnement et les diagnostics lorsque la clé API est disponible, sans bloquer le workflow si le service LLM est indisponible.
