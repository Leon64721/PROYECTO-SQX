# ERROR CRÍTICO: "There is no Price block defined!" — Diagnóstico Inmediato

**Fecha:** 2026-09-21, 11:12:40  
**Proyecto:** NDXm_ORB_PropFirm_V3_MTF_CLEAN  
**Error:** `com.strategyquant.tradinglib.generator.GenerateException: There is no Price block defined!`  
**Estado:** 🔴 BUILD FALLIDO — 0 estrategias generadas en 40s

---

## ANÁLISIS DEL ERROR

### Línea de Error en Log
```
11:12:40 BS-NDXm_ORB_MTF : com.strategyquant.tradinglib.generator.GenerateException: 
  There is no Price block defined!
  at com.strategyquant.tradinglib.blocks.random.ReplacementConfig.chooseSpecialRandomly(Unknown Source)
  at ... ReplacementConfig.generateSpecialBlock(Unknown Source)
  at ... ReplacementParameter.addFormulaPriceParam(Unknown Source)  ← AQUÍ: intenta crear Price param
```

### ¿Qué significa?

El motor de generación intenta crear una estrategia e:
1. Busca un **Random Group con tipo VALUE** (Price block/price levels)
2. **NO ENCUENTRA NINGUNO** configurado en el proyecto
3. Falla al intentar generar parámetros de precio
4. Abortada toda la generación

### Timeline del Build
```
11:11:59 Loading backtest data
11:12:39 Creating backtest data feed  
11:12:40 All backtest data prepared ✓ (datos OK)
11:12:40 Generating initial population for islands #1-7
11:12:40 ERROR: There is no Price block defined! ✗ (genera fallida)
11:12:40 Finished in 40s (Build aborted)
11:12:40 Retest1: No strategies to retest (cascading failure)
```

---

## CAUSA RAÍZ: ¿Dónde está el Price Block?

### Lo que falta
El proyecto V3_MTF_CLEAN necesita UN O MÁS **Random Groups con tipo VALUE**:
- `Levels_ORB_NDXm` (Price levels: High/Low/HighD/LowD)
- O cualquier otro grupo de niveles de precio

### ¿Por qué V2 también falla?

Cuando clonamos V2 → V3, copiamos el `project.cfx` (XML) pero:
- El XML contiene REFERENCIAS a Random Groups por UUID
- Si los UUID referenciados no existen en la instalación, SQX no los encuentra
- O el XML nunca tuvo esos grupos configurados

### Evidencia
- V2 nunca fue ejecutado antes (fue creado el 2026-09-16 pero no testeado)
- V3 heredó la config incompleta de V2
- Esta es la MISMA CAUSA que V4 (INDEX.md fila 50 menciona "0 Price blocks")

---

## COMPARACIÓN: ¿QUÉ TIENE V8 ORB QUE V3 NO TIENE?

Según el índice, ORB V8 SÍ funciona (541/1800 OOS sobrevivientes). 

**V8 tiene:**
- Custom blocks: ORBLongBreakout, ORBShortBreakout, PropFirmCompliance
- Random groups: Breakout_Triggers, PropFirmComplianceFilters
- **Y CRÍTICO:** Un **Random Group VALUE** para niveles de precio

**V3 está missing:**
- La configuración del **Random Group VALUE** (Levels_ORB_NDXm)
- O el UUID del grupo existe en XML pero el grupo no está importado en SQX

---

## SOLUCIÓN PROPUESTA

### Opción A: Usar ORB V8 como base (RECOMENDADO)
V8 ya funciona (541/1800 OOS). En lugar de depurar V3:
1. Copiar `BASE_CP_MASTER_CLEAN_V1_ORB_V8_AVGTRADE_SL.cfx`
2. Cambiar símbolo M15 a NDXm
3. Ejecutar Build → OOS
4. **Tiempo:** 30 min

**Ventaja:** Bypass del problema, reutilizar config probada

### Opción B: Reparar V3 (FIX)
1. Verificar XML del proyecto.cfx
2. Buscar referencias a UUIDs de Random Groups
3. Si faltan, importar `Levels_ORB_NDXm` en AlgoWizard
4. Guardar proyecto
5. Reintentar Build
6. **Tiempo:** 45+ min, con riesgo de cascada

### Opción C: Regenerar desde sqx-strategy-project (NUCLEAR)
1. Re-generar V3 desde las skills sqx-*
2. Asegurar que todos los Random Groups se inyecten en el .cfx
3. **Tiempo:** 90 min

---

## RECOMENDACIÓN

**Opción A es la más rápida y segura:**
- Usamos el proyecto ORB V8 que ya comprobamos que genera 1800 estrategias
- Solo ajustamos símbolo/timeframe
- Ejecutamos Build → OOS con una línea base probada
- **Riesgo:** BAJO (V8 ya funciona)

---

## PRÓXIMO PASO

**¿Cuál opción prefieres?**

1. **Opción A:** Usar ORB V8 (rápido, bajo riesgo)
2. **Opción B:** Reparar V3 (investigación + fix)
3. **Opción C:** Regenerar desde cero (lento pero garantizado)

**Mi recomendación:** Opción A → ejecutar en 30 min → tenemos resultado de FASE 1

---

**Estado:** Bloqueado en decisión del usuario  
**Error:** Confirmado y documentado  
**Causa:** Missing Price block en V3 (heredado de V2)
