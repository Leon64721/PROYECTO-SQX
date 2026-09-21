# Plan: Generar Custom Project Desde Cero — 2026-09-21

**Objetivo:** Crear NDXm_ORB_PropFirm_FASE1_V0 completamente nuevo, evitando herencia de V2/V3

**Ruta:** skills locales sqx-* (no clones ni herencias)

---

## FASE A: Generar Random Groups (Price Blocks)

**Skill:** `sqx-random-group`

### 1. Crear `Levels_ORB_NDXm` (Value group)

```
type: Value (price levels)
items:
  - Highest[1]     (prior day high)
  - Lowest[1]      (prior day low)
  - PriorDayHigh   (built-in, prior day close high)
  - PriorDayLow    (built-in, prior day close low)
  - HighD[1]       (current day high so far)
  - LowD[1]        (current day low so far)
```

**Output:** `Levels_ORB_NDXm.xml` → import en AlgoWizard

---

## FASE B: Generar Strategy Template (Multi-Temporal)

**Skill:** `sqx-strategy-template`

### Spec: `NDXm_ORB_MTF`

```json
{
  "name": "NDXm_ORB_MTF",
  "shape": "mtf_filter",
  "daily_filter": "FilterTrendDirection_ORB",
  "trigger": "EntriesBreakout_ORB",
  "price_pool": "Levels_ORB_NDXm",
  "roles": {
    "FilterTrendDirection_ORB": "daily regime (D1)",
    "EntriesBreakout_ORB": "intraday breakout trigger (M15)",
    "Levels_ORB_NDXm": "stop level (prior period H/L)"
  },
  "thesis": "ORB en M15 filtrado por tendencia diaria = mayor follow-through"
}
```

**Output:** `NDXm_ORB_MTF.sqx` → embebida en el proyecto

---

## FASE C: Generar Custom Project (.cfx completo)

**Skill:** `sqx-strategy-project`

### Config:

```
Base project: (donor con datos NDXm, settings prop firm)
Template: NDXm_ORB_MTF.sqx
Output databanks: BS-NDXm-MTF (Build), Retest-1-7 (OOS/MC/SPP/WFA)
Overrides:
  - instrument: NDXm_TICK_UTCPlus02
  - dates: 2018-06-27 a 2026-06-25
  - trading:
      spread: 80
      slippage: 1
      session: 01:00 - 23:30 EET (NY 16:30-22:30 durante horario)
  - generation:
      databank_cap: 1800
      acceptance: ["AvgTradesPerMonth"]  (mantener todos, no filtrar por ProfitFactor)
```

**Output:** `NDXm_ORB_PropFirm_FASE1_V0.cfx` → listo para SQX

---

## Checkpoint: ¿Qué diferencia a este del V3 fallido?

| Aspecto | V3_MTF_CLEAN (fallido) | FASE1_V0 (nuevo) |
|--------|----------------------|-----------------|
| Origen | Clon byte-a-byte de V2 | Generado por skills |
| Price blocks | Heredados (faltantes) | **Generados explícitamente** |
| Random groups | XML residual de V2 | Fresh, validados |
| Build-Task | Donor de V2 clonado | Nuevo, con template limpio |
| Validación | Solo estructura XML | Skills engine + AlgoWizard validate |

---

## Orden de Ejecución

1. **Generar `Levels_ORB_NDXm.xml`** (sqx-random-group)
   - ~5 min
   - Import en AlgoWizard
   
2. **Generar `NDXm_ORB_MTF.sqx`** (sqx-strategy-template)
   - ~10 min
   - Valida que los grupos existan
   
3. **Generar `.cfx` proyecto completo** (sqx-strategy-project)
   - ~15 min
   - Deploy en C:\SQX_144_Full\user\projects
   - **Cierra SQX primero**
   
4. **SQX Build → OOS** (monitoreo en vivo)
   - ~1 hora total
   - CHECKPOINT: ¿Sobrevivientes > 0?

---

## Riesgo y Mitigación

| Riesgo | Mitigación |
|--------|------------|
| Skills no encuentran groups | Verificar `catalog.json` antes |
| Template no resuelve | Validar `discover.py` output |
| .cfx deployment falla | SQX debe estar cerrado + backup |
| Build aún falla con Price block | Revisar XML del .cfx generado |

---

## Go/No-Go

✅ **GO si:**
- Skills están disponibles en `.claude/skills/sqx-*`
- `catalog.json` existe y tiene los groups base
- Usuario confirma cerrar SQX antes de deploy

❌ **NO-GO si:**
- Skills no están configuradas
- Install path no se puede resolver

---

**Siguientes pasos:** Confirmación del usuario → ejecutar FASE A

