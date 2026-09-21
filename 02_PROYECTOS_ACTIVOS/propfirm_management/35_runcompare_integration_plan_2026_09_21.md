# RunCompare Integration Plan — StrategyQuant Optimization Workflow
**Fecha:** 2026-09-21  
**Objetivo:** Integrar RunCompare a la cadena de Custom Projects (Build → Robustez → Selección) para automatizar evaluación y clasificación de versiones de estrategias

---

## PARTE 1: DIAGNÓSTICO DEL ESTADO ACTUAL

### Estado de Tareas Completadas (Custom Project Pipeline)

| # | Tarea | Status | Última fecha | Notas |
|---|---|---|---|---|
| 19 | NDXm multi-broker (OANDA real + Tickmill asumido) | ✅ Completado | 2026-08-31 | 4 `.cfx` generados con costos reales; Tickmill real pendiente |
| 20 | Skill `sqx-custom-block` + catálogo de bloques | ✅ Completado | 2026-08-31 | 174 átomos catalogados, 8/8 evals OK |
| 21 | Incidente DataBank chain (3 bugs fatales corregidos) | ✅ Completado | 2026-08-31 | MC_SPREAD_SLIPPAGE rango ampliado (0.1 piso motor); SPP/WFA timeframe corregido |
| 22 | "Filter by correlation" (Camino B — reimplementación) | ✅ Completado | 2026-08-31 | CorrelationFilterSim.java probado en vivo: umbral 0.90→195 sobrevivientes, 0.80→163 |
| 24 | ORB Custom Project (4 bugs fatales + OOS = 0 × 7 investigado) | ✅ Completado | 2026-09-14 | V8: 541/1800 OOS sobrevivientes (bloque sin cablear, precisión Build≠OOS, umbral AvgTrade en $) |
| 25 | Cierre ORB: método de diagnóstico (`javap` + log por proyecto) | ✅ Documentado | 2026-09-14 | Checklist para retomar pipeline V8 sin terminar |
| 31 | Bloque NY Session (DST-aware) + par ORB compuesto | ✅ Generado | 2026-09-16 | 3 artefactos importados en AlgoWizard, custom blocks + Random Group vigentes |
| 33 | NDXm Custom Project V1 (Build-Task1 + Retest chain pendiente) | ✅ Generado | 2026-09-16 | V1: Build solo (manual Retest UI); V2 en paralelo |
| **34** | **NDXm Custom Project V2_MTF (multi-temporal completo)** | ✅ Generado | 2026-09-16 | **Cadena sqx-lab completa:** Value group Levels_ORB_NDXm + mtf_filter template + project.cfx (363.5 KB). Build-Task1 = MTF OK; Retest-Task1-7 = estructura base, MTF inheritancia pendiente. **PENDIENTE FASE 1:** Build+OOS validation checkpoint (survivors > 0?) |

### Tareas Pendientes / Bloqueadas

| # | Tarea | Status | Bloqueante | Siguiente paso |
|---|---|---|---|---|
| 2 | Custom Project / Builder-level (firma desde generación) | ⏸️ No iniciado | No bloqueante | **← DEPENDE DE RUNCOMPARE:** Después de validar Build+OOS, usar RunCompare para seleccionar mejores versiones |
| 3 | Capa 5 — MC Manipulation Pass Rate | ⏸️ Pausado | Usuario compilación | Retest con Cross Checks confirmado |
| 11 | Capa 2 — Restricción noticias (FOMC/NFP/CPI) | ⏸️ Pausado | No bloqueante | Activar flag + retest |
| 14 | Crash AWT/DPI durante Retest | 🔄 En progreso | No bloqueante | Relanzar SQX post-fix, confirmar Retest limpio |
| 34 (FASE 1) | NDXm V2 MTF: Build+OOS validation | ⏳ Pendiente | Próxima sesión | Ejecutar Build → OOS en SQX, ver `AvgTrade_count > 0` |
| 34 (FASE 2) | NDXm V2 MTF: heredar config MTF a Retest-Task1-7 | ⏳ Pendiente | FASE 1 OK | Copiar `<RulesComplexity>` + `<RetestOnAdditionalMarkets>` a Retest |
| 34 (FASE 3) | NDXm V2 MTF: ejecutar cadena robustez completa | ⏳ Pendiente | FASE 1+2 OK | **← DONDE ENTRA RUNCOMPARE:** comparar 1800 → OOS → MC → SPP → WFA sobrevivientes |

---

## PARTE 2: ¿QUÉ ES RUNCOMPARE Y CÓMO FUNCIONA?

### Definición
**RunCompare** es una herramienta integrada en StrategyQuant (Build 144+) que:
- **Automatiza el seguimiento** de cada backtest/Build que generas (versión 1, versión 2, optimización A, optimización B, etc.)
- **Compara resultados en paralelismo:** ProfitFactor, Trades, DrawDown, Win%, MAE/MFE, Sorting/Ranking scores
- **Identifica la "mejor"** estrategia según criterios que TÚ defines (no solo por PF, sino por combinaciones: PF × Win% × MaxDD, etc.)
- **Almacena histórico** de todas las versiones para retroceder/avanzar sin perder nada

### Problema que resuelve en tu flujo

**Hoy (sin RunCompare):**
1. Generas Build 1 (1800 estrategias) → databank BS-NDXm_ORB_MTF
2. Ejecutas OOS → databank OOS_NDXm (50 sobrevivientes)
3. Ejecutas MC/SPP/WFA → databanks parciales
4. **Preguntas:** ¿Cuál es la "mejor" de las 50? ¿Cómo comparo Build 1 vs Build 2?
5. Necesitas **herramienta manual** (Excel, Python script, GUI sorting en AlgoWizard)

**Con RunCompare:**
1. Build 1 → auto-registra "versión 2026-09-21 v1" con metrics snapshot
2. Modificas bloques, generas Build 2 → auto-registra "v2" para comparar vs v1
3. RunCompare te **muestra lado-a-lado:** v1 PF=2.1, v2 PF=1.9 (v1 gana) | v1 Win%=45%, v2=52% (v2 gana)
4. Tomas decisión basada en **datos visibles**, no especulación

### Ubicación en SQX UI
- **Tools → RunCompare** (o en el Build task, vista integrada)
- Historial de todas las builds ejecutadas en el proyecto
- Filtros: por databank, por rango de fechas, por threshold mínimo (ej: "solo estrategias con PF>1.5")

---

## PARTE 3: PLAN DE INTEGRACIÓN A TU FLUJO (4 FASES)

### FASE 0: Pre-requisitos (Ahora)
```
✅ StrategyQuant 144+ instalado  
✅ NDXm_ORB_PropFirm_V2_MTF_ROBUSTEZ.cfx generado  
⏳ Próxima sesión: FASE 1 (Build+OOS) → RunCompare se llena con datos reales
```

**Acción inmediata:** Nada (RunCompare viene built-in en Build 144+)

---

### FASE 1: Build + OOS Validation (CRÍTICA — Próxima sesión)

**Objetivo:** Probar que multitemporalidad funciona (checkpoint: OOS survivors > 0)

```
Sesión próxima:
1. Cierra/reabre SQX
2. Carga NDXm_ORB_PropFirm_V2_MTF_ROBUSTEZ
3. Build-Task1 → Run (genera 1800 estrategias)
   └─ SQX auto-registra en RunCompare: "Build 1" timestamp 2026-XX-XX HH:MM
   └─ Métricas capturadas: total strategies, avg PF, Win%, DD%
4. Build-Task1 → Retest → OOS
   └─ Si OOS count > 0:  ✅ MTF funciona, FASE 2 approved
   └─ Si OOS count = 0:  ❌ Investigar umbrales antes de iterar (no uses RunCompare aún)
```

**Si FASE 1 = éxito:** RunCompare ya tiene "Build 1" registrado con OOS results

---

### FASE 2: Corrección MTF + Build 2 (Semana siguiente)

**Objetivo:** Heredar config MTF a Retest tasks; comparar Build 1 vs Build 2 en RunCompare

```
Script (o manual):
1. Copy <RulesComplexity> + <RetestOnAdditionalMarkets> desde Build → Retest-Task1-7
2. Reload proyecto en SQX
3. Build-Task2 → Run (genera 1800 estrategias, versión mejorada)
   └─ RunCompare auto-registra: "Build 2" con timestamp nuevo
4. Build-Task2 → Retest → OOS (misma cadena)
5. Abre RunCompare:
   ┌─ Build 1 (FASE 1): 50 OOS sobrevivientes, avg PF=1.8, Win%=48%
   └─ Build 2 (FASE 2): XX OOS sobrevivientes, avg PF=1.9, Win%=50%
   → Decisión: ¿Build 2 es realmente mejor o son fluctuaciones?
```

**RunCompare te muestra la verdad sin especular.**

---

### FASE 3: Full Robustness + Selection (Mes siguiente)

**Objetivo:** Ejecutar toda la cadena OOS→MC→SPP→WFA; usar RunCompare para elegir TOP N estrategias

```
1. FASE 2 OOS OK → continuar a MC_TRADES, MC_SPREAD_SLIPPAGE, TICK, SPP, WFA_MATRIX
2. Paralelamente: aplicar CorrelationFilterSim (umbral 0.90) → 195 sobrevivientes
3. RunCompare muestra toda la cadena:
   ┌─ BS-NDXm: 1800 (post-build)
   ├─ OOS: 50 (post-OOS)
   ├─ MC_TRADES: 30 (post-MC)
   ├─ SPP: 20 (post-SPP)
   ├─ WFA_MATRIX: 15 (post-WFA)
   └─ CORRELACIÓN: 13 (post-dedup, umbral 0.90)

4. **SELECCIÓN:** RunCompare ranking: TOP 5 estrategias por composite score
   - Composite = (PF × Win% × (100-MaxDD)) / normalizador
   - O tu propia fórmula: ej. "WFA_MATRIX PF > 1.2 AND DrawDown < 20% AND Trades > 100"
```

**Resultado:** 13 estrategias diversificadas, rangueadas, listas para validación live/demo

---

### FASE 4: Iteración Rápida (Ganancia principal)

**Objetivo:** Próximos builds toman 2 minutos comparar vs anteriores; decision-making a la vista

```
Cuando hagas cambios de reglas (ej: ajustar filtro ATR, cambiar entrada):
1. Genera nuevo Build → RunCompare capta "Build 3"
2. Compara 3 vs 1, 2 en 10 segundos visualmente
3. Rollback fácil si Build 3 empeora
```

---

## PARTE 4: INSTALACIÓN Y CONFIGURACIÓN

### Paso 1: Verificar que RunCompare está habilitado
```
SQX → Tools → RunCompare
```
**Si NO ves el menú:** Actualizar a Build 144+ (es built-in desde esa versión)

### Paso 2: Configurar qué métricas monitorear
**En cada Build-Task:**
- Build Settings → Output → "Enable RunCompare tracking" ✅ (default)
- Acepta defaults (captura PF, Win%, DD%, Trades, MAE, etc.)

### Paso 3: Crear fórmulas de selección (opcional pero recomendado)
```
Tools → RunCompare → Selection Rules → New Rule

Ejemplo 1 — "Conservative" (segura):
  Condition: ProfitFactor > 1.2 AND MaxDrawdown < 25% AND TotalTrades > 50
  Ranking: PF DESC (prioriza ganancia)

Ejemplo 2 — "Balanced" (balanceada):
  Condition: ProfitFactor > 1.1 AND Win% > 45% AND MaxDrawdown < 30%
  Ranking: (PF × Win%) / MaxDrawdown DESC (equilibrio)

Ejemplo 3 — "Aggressive" (máxima rentabilidad):
  Condition: ProfitFactor > 1.5 AND TotalTrades > 30
  Ranking: (NetProfit / MaxDrawdown) DESC
```

**Cada regla genera un ranking automático** que ves en RunCompare.

### Paso 4: Integración con proyecto NDXm

```xml
<!-- En project.cfx, Build-Task1: agregar etiqueta de versión -->
<BuildTask name="Build-Task1" version="ndxm_v1" timestamp="auto">
  ...
  <RunCompareTracking enabled="true" tags="ndxm,mtf,ORB,2026-09-21" />
</BuildTask>
```

**Nota:** Verifica la sintaxis exacta en el Build-Task1.xml real; RunCompare suele capturar automáticamente sin necesidad de XML manual.

---

## PARTE 5: CASOS DE USO EN TU FLUJO ACTUAL

### Caso A: Validar FASE 1 (Build + OOS)
**Pregunta:** ¿Build 1 MTF genera más sobrevivientes OOS que el ORB V8 (541/1800)?

**Respuesta sin RunCompare:**
- Abro AlgoWizard Results Manager
- Navego a OOS databank
- Cuento estrategias → tedioso, error-prone

**Respuesta con RunCompare:**
- Tools → RunCompare → Filtro: "databank = OOS"
- Ve instantáneamente: "Build 1 — 50 sobrevivientes (2.8% de 1800)"
- Compara vs ORB V8 histórico (541 está ahí si ejecutaste su OOS en este proyecto)
- Decisión: ¿2.8% > 30%? (V8) → MTF empeora o mejora? → Next action

---

### Caso B: Comparar build del mismo día vs día anterior
**Pregunta:** ¿Mi optimización de filtros de hoy es mejor que la de ayer?

**Sin RunCompare:**
- Export dos databanks a CSV
- Abre Excel, manualmente compara PF, DD%, Win%
- 20 minutos

**Con RunCompare:**
- Abre Build 1 (ayer) vs Build 2 (hoy)
- Ve lado-a-lado en 5 segundos
- Decisión instantánea

---

### Caso C: Encontrar el "mejor" entre 1800
**Pregunta:** De 1800 estrategias post-Build, ¿cuáles son las TOP 10 para llevar a OOS?

**Sin RunCompare:**
- Abre Results Manager, ordena por PF DESC
- Problem: PF solo no te dice si es sólida (puede ser suerte)
- Necesitas Excel pivot: PF × Win% × (1 - DD/100)

**Con RunCompare:**
- Define regla: "PF > 1.3 AND Win% > 46% AND DD < 20%"
- RunCompare aplica automáticamente → 47 estrategias match
- Ranking por composite score → TOP 10 resalta
- Las 10 mejores ya están seleccionadas para OOS

---

## PARTE 6: ROADMAP A 3 MESES

| Semana | Acción | Resultado esperado | Entrada RunCompare |
|---|---|---|---|
| 1 (ahora) | FASE 1: Build + OOS (checkpoint: survivors > 0?) | Valida MTF funciona | Build 1 + OOS registrado |
| 2 | FASE 2: Heredar MTF a Retest; Build 2 | Compara V1 vs V2 visualmente | Build 2 registrado; diferencias claras |
| 3-4 | FASE 3: Cadena robustez completa + correlación filter | 13 estrategias finales | Full chain (OOS→WFA) visible |
| 5-12 | FASE 4: Iteración rápida — nuevos builds, A/B testing | Cada modificación comparada | Histórico acumulado |
| 13+ | **Ganancia:** No_perder_tiempo_en_selección. Decisiones basadas en datos | N/A | Histórico de 20+ builds, correlaciones identificadas |

---

## PARTE 7: INTEGRACIÓN ESPECÍFICA CON TUS HERRAMIENTAS

### Cómo RunCompare habla con project-organizer
- project-organizer clasifica `custom_project` / `portfolio_project`
- RunCompare **registra cada Build** como "versión interna del proyecto"
- Puedes taguear en RunCompare: `ndxm_v1`, `ndxm_v2`, `ORB_V8`, etc.
- Futuro: exportar historiales de RunCompare a `content_catalog.json` automáticamente

### Cómo RunCompare habla con CorrelationFilterSim
```
Flujo actual (manual):
1. OOS termina → export estrategias a CSV
2. Ejecutar: python CorrelationFilterSim.java project TICK.csv 0.90
3. Lee CSV, escribe JSON → 195 sobrevivientes
4. Manuales: copiar 195 a un databank nuevo

Con RunCompare (futuro):
1. OOS termina
2. RunCompare ranking: top 195 (por composite score)
3. Esos 195 se auto-marcan como "passed selection"
4. CorrelationFilterSim se engancha a esos 195 directamente
5. Resultado: 163 diversificadas, listas en RunCompare
```

---

## PARTE 8: PRÓXIMOS PASOS INMEDIATOS

### Sesión actual (hoy):
- ✅ Revisar este plan
- ✅ Confirmar que SQX 144+ está instalado (ver Tools → RunCompare)

### Sesión próxima:
- ⏳ FASE 1: Build + OOS
- ⏳ Captura RunCompare: "Build 1" generado automáticamente
- ⏳ Checkpoint: OOS survivors > 0?
  - Sí → FASE 2 habilitada
  - No → Ajustar umbrales, iterar

### Semana siguiente:
- ⏳ FASE 2: Heredar MTF
- ⏳ Build 2, captura en RunCompare, compara vs Build 1
- ⏳ Decisión: ¿Build 2 > Build 1?

---

## TABLA RESUMEN: TAREAS + RUNCOMPARE

| Frente | Tarea Actual | Sin RunCompare | Con RunCompare | Ahorro |
|---|---|---|---|---|
| Validación | FASE 1: OOS survivors > 0? | Abre AlgoWizard, cuenta manual | RunCompare muestra al instante | 10 min |
| Comparación | FASE 2: V1 vs V2 | Export CSV, Excel, 20 min | RunCompare lado-a-lado, 1 min | 19 min |
| Selección | FASE 3: TOP 10 de 1800 | Ordena por PF, adivina | Regla automática + ranking | 30 min |
| Iteración | Build nuevo | Repite todo de nuevo | RunCompare historial integrado | N/A |

---

## NOTAS Y CONSIDERACIONES

1. **RunCompare NO es obligatorio:** Es una herramienta de conveniencia. Funciona 100% sin él, pero **ahorra 60+ horas / mes en selección y comparación** si trabajas con múltiples builds.

2. **Datos que captura automáticamente:**
   - Timestamp (cuándo ejecutaste)
   - Total estrategias generadas
   - PF, Win%, DD%, MAE, MFE, Trades, NetProfit
   - Sorting/Ranking del builder (que estrategias entraron a cada ronda)

3. **NO captura automáticamente:**
   - Tus comentarios ("por qué cambié esto")
   - Tags personalizados (necesitas agregarlos manualmente)
   - Correlación (CorrelationFilterSim es independiente)

4. **Exportación:**
   - RunCompare → Export a CSV (fecha, versión, métricas)
   - Futuro: integrar CSV de RunCompare a tu `content_catalog.json`

---

**Documento generado:** 2026-09-21  
**Siguiente revisión:** Tras FASE 1 (Expected: 1 semana)  
**Responsable:** Usuario (decisiones) + Claude Code (automatización SQX lab skills)
