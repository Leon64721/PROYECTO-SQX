# MANIFEST — FUENTES LIMPIAS SQX CUSTOM PROJECTS — OOS 20–30 + EXISTING SESSION + SHORTNAME SAFE

## Paquete

`SQX_PROJECT_SKILLS_OOS_20_30_EXISTING_SESSION_SHORTNAME_SAFE_20260517`

## Motivo de esta actualización

Se corrige definitivamente el flujo de generación/importación de Custom Projects cuando intervienen sesiones de broker en StrategyQuant X.

Incidente validado:

```text
GBPUSD DooPrime Cent:
- V3 falló por sesión inferida con corchetes.
- V4 falló por incrustar una sesión existente como recurso nuevo.
- V5 abrió sin sesión embebida.
- V6 abrió E1/E2 con sesión existente, pero E3 falló por Project name largo.
- V7 funcionó en los 4 customs con sesión existente, <Sessions /> vacío, LimitTimeRange=false y nombres cortos.
```

## Fuentes activas definitivas

1. `01_SKILL_1_GENERADOR_CFX_SQX_V1_9_OOS_20_30_OPERATORS_EXISTING_SESSION_SHORTNAME_SAFE_RESOURCE_QG.md`
2. `02_SKILL_2_MOTOR_VALIDACION_ROBUSTA_SQX_V1_5_OOS_20_30_SESSION_SHORTNAME_COMPAT.md`
3. `03_SKILL_3_CUSTOM_PROJECT_ORCHESTRATOR_QA_V1_12_OOS_20_30_EXISTING_SESSION_SHORTNAME_SAFE.md`
4. `04_SKILL_4_CUSTODIA_BASE_CUSTOM_PROJECTS_LIMPIOS_V1_10_OOS_20_30_EXISTING_SESSION_SHORTNAME_SAFE.md`
5. `05_BASE_CFX_RUTAS_TODO_DICCIONARIO_NODOS_BUILDER.csv`
6. `06_RANKING_FILTROS_SQX_DICCIONARIO_METRICAS.json`
7. `07_BASE_CUSTOM_PROJECT_MASTER_CLEAN_SQX_V1_SOURCE_ONLY.cfx`
8. `08_MANIFEST_FUENTES_LIMPIAS_SQX_CUSTOM_PROJECTS_OOS_20_30_EXISTING_SESSION_SHORTNAME_SAFE.md`
9. `09_README_ACTUALIZACION_EXISTING_SESSION_SHORTNAME_SAFE.md`
10. `10_CHANGELOG_INCIDENTE_GBPUSD_DOOPRIME_SESION_NOMBRES_CORTOS.md`

## Reemplazos

- Skill 1 V1.9 reemplaza V1.8.
- Skill 2 V1.5 reemplaza V1.4.
- Skill 3 V1.12 reemplaza V1.11.
- Skill 4 V1.10 reemplaza V1.9.
- Base `.cfx`, diccionario de rutas/nodos y diccionario de métricas se conservan.

## Reglas bloqueantes nuevas

```text
1. No sintetizar sesión usando broker profile.
2. No incrustar <Session> de broker existente sin donor .cfx probado.
3. Si la sesión existe en Data Manager: usar nombre literal como referencia funcional y dejar <Sessions /> vacío.
4. LimitTimeRange=true solo con donor .cfx probado.
5. No usar Add new para sesiones existentes.
6. Project name interno preferido <=25 caracteres y máximo <=30.
7. No reutilizar Project name de versiones fallidas.
8. Importar desde ruta corta C:\SQX_IMPORT\.
```

## Auditorías obligatorias acumuladas

1. StrategyFile Resource Safe.
2. Operators Safe.
3. Session Existing Resource Safe.
4. Donor Session Gate.
5. ShortNameSafe.
6. DataBank Chain.
7. Symbol Resource Exact.
8. Anti-residuos global.
9. Builder Quality Gate.
10. Multi-Timeframe Quality Gate.
11. OOS 20–30 Audit.

## Uso recomendado

Usar este paquete completo y retirar el paquete anterior `OOS_20_30_SESSION_SAFE` para evitar que se vuelvan a generar proyectos con sesiones incrustadas o nombres largos.
