# Cierre de Sesión — 2026-09-21: Diagnóstico V5 + Plan de Recovery

**Fecha:** 2026-09-21  
**Duración:** ~2 horas (diagnóstico sin código)  
**Resultado:** ✅ Causa raíz encontrada, plan ejecutado, V3_MTF_CLEAN listo para FASE 1

---

## RESUMEN EJECUTIVO

### Problema
- **V5_LONG** proyecto generado 2026-09-17 falla en Build: `Cannot create strategy from XML! Block doesn't contain item 1` (70%+ excepciones)
- **V5_SHORT** nunca se creó en disco
- Usuario preguntaba: "¿Qué pasó con QlibSignal en 'Trading signals'?"

### Causa Raíz (CONFIRMADA)
**V5_LONG generado CON ESTRUCTURA XML INCOMPLETA:**
- Build-Task1.xml tiene 4 `<signal>` elements pero solo signal[0] tiene contenido
- Signals[1-3] están VACÍOS vs V2 donde todas tienen contenido
- Cuando Build intenta acceder item 1 en signals vacíos → falla

### Decisión Tomada
✅ **OPCIÓN A:** Archivar V5 como obsoleto → Clonar V2 como V3_MTF_CLEAN → Validar en SQX FASE 1

### Resultado Ejecutado
✅ V3_MTF_CLEAN creado (clon exacto de V2, 380.612 bytes)  
⏳ Próxima sesión: Build → OOS checkpoint (survivors > 0 = ventana ORB FUNCIONA)

---

## INVESTIGACIÓN TÉCNICA

### Extracción y Análisis de XML

```
V5_LONG.cfx (ZIP) → Build-Task1.xml (2,232,557 bytes)
V2_MTF_ROBUSTEZ.cfx (ZIP) → Build-Task1.xml (2,245,912 bytes)
```

**Signal[0]:** ✓ Idénticos en ambos (2 RandomConditions)
**Signal[1-3]:** ✗ V5 vacíos vs ✓ V2 llenos

#### V5 Signal[1] (VACÍO)
```xml
<signal variable="33333333-2222-1111-3333-333333333333" />
```

#### V2 Signal[1] (LLENO)
```xml
<signal variable="33333333-2222-1111-3333-333333333333">
  <Item key="AND">
    <Block>
      <Item key="RandomCondition" ...>
        <!-- Contenido presente -->
      </Item>
    </Block>
  </Item>
</signal>
```

### Impacto
- V5 Build intenta materializar estrategias
- Signal[0] = OK (2 items, puede acceder item 0 y 1)
- Signal[1-4] = FAIL (vacías, intenta acceder item 1 → no existe)
- **Result:** 70%+ de estrategias lanzan excepción → Build se detiene

---

## CLARIFICACIÓN: QlibSignal NO fue el problema

**Usuario confirmó:** "QlibSignal fue accidente. Intent original: ORB wizard + multitemporalidad"

**Hallazgo:** QlibSignal EXISTE en AMBOS proyectos (V5 y V2) como bloque utilizable, pero **no es la causa del error** en "Trading signals". El error es estructura XML incompleta, no un bloque faltante.

---

## PLAN EJECUTADO: FASE A-B-C

### FASE A ✅ DIAGNOSTICO (Investigación sin código, 30 min)
1. Extrajimos ambos proyectos `.cfx` (son ZIPs)
2. Comparamos Build-Task1.xml de V5 vs V2 línea por línea
3. Encontramos signals[1-3] vacíos en V5
4. Confirmamos que la estructura es el problema, no QlibSignal

**Documentación:** `37_DIAGNOSTICO_FASE_A1_V5_vs_V2_2026_09_21.md`

### FASE B ✅ ARCHIVADO (project-organizer)
1. Marcamos V5_LONG como `obsoleto_no_recuperable` en INDEX.md
2. Documentamos causa raíz para referencia histórica
3. **NO borramos V5** — conservado como lección (evitar repetir generaciones incompletas)

### FASE C ✅ VALIDACION (Clone + prep para SQX)
1. Clonamos V2 → V3_MTF_CLEAN (copia byte-a-byte)
2. Verificamos integridad: 380.612 bytes iguales
3. Ubicación lista: `C:\SQX_144_Full\user\projects\NDXm_ORB_PropFirm_V3_MTF_CLEAN`
4. **Próxima sesión:** Abrir en SQX, Build → OOS

---

## CHECKPOINT CRÍTICO (PRÓXIMA SESIÓN)

### FASE 1: Build + OOS Validation

**Ejecutar:**
1. Cierra SQX (si está abierto)
2. Reabre SQX
3. File → Open → NDXm_ORB_PropFirm_V3_MTF_CLEAN
4. Verifica Build-Task1 carga sin errores
5. **Build → Run** (~1800 estrategias)

**CHECKPOINT:**
- ¿Build genera 1800 estrategias SIN excepciones?
  - **SÍ** → Continúa a OOS
  - **NO** → Investigar (diferente causa que V5)

- ¿OOS produce sobrevivientes > 0?
  - **SÍ** ✅ → **Ventana ORB anclada a apertura NY real FINALMENTE FUNCIONA** (4 intentos después)
  - **NO** ❌ → Ajusta umbral: DrawdownPct 35% → 40-45% (modo DISCOVERY no ESTRICTO)

---

## GOBERNANZA Y PROTOCOLOS

### Lección Aprendida
- No usar `sqx-strategy-project` con bases/templates **incompletos**
- Siempre verificar que el donor de un clon tiene todos los elementos poblados
- Conservar artifacts obsoletos en INDEX.md + archivado (no borrar)

### Regla Nueva
Cuando un proyecto falla con "Block doesn't contain item X":
1. Extraer `.cfx` (es ZIP)
2. Comparar `<Rule>` / `<signals>` vs un proyecto probado
3. Verificar que todos los elements están llenos (no vacíos)
4. **NUNCA** asumir que es un bloque faltante — puede ser estructura incompleta

---

## ARCHIVOS GENERADOS ESTA SESIÓN

| Archivo | Propósito | Estado |
|---------|-----------|--------|
| `36_PLAN_DIAGNOSTICO_Y_RECUPERACION_V5_2026_09_21.md` | Plan estructurado FASE A-B-C | ✅ Documentado |
| `37_DIAGNOSTICO_FASE_A1_V5_vs_V2_2026_09_21.md` | Análisis técnico detallado | ✅ Documentado |
| `38_CIERRE_SESION_2026_09_21...` (este archivo) | Resumen + próximos pasos | ✅ En progreso |
| INDEX.md (filas 35-36) | Actualizado con investigación | ✅ Actualizado |

---

## PRÓXIMO PASO INMEDIATO

### Dentro de ~24 horas (cuando el usuario esté listo para FASE 1):
1. Cierra/reabre SQX
2. Abre V3_MTF_CLEAN
3. Build → Run
4. RunCompare captura "Build 1" automáticamente
5. OOS validation → **checkpoint decisivo: survivors > 0?**

### Si FASE 1 = Éxito
- Documentar: "V3 clon de V2 funciona. Ventana ORB confirmada."
- Pasar a FASE 2: heredar MTF en Retest tasks
- Agenda: semana siguiente

### Si FASE 1 = Fallo
- No asumir nada — verificar log de SQX línea por línea
- Buscar % exacto de fallos en Failed details
- Considerar umbral de aceptación OOS (actualmente 35%, quizá 40-45%)

---

**Sesión cerrada:** 2026-09-21, 22:30 UTC  
**Estado proyecto:** V3_MTF_CLEAN listo, diagnóstico completo, plan ejecutado sin errores  
**Próximo hito:** FASE 1 Build + OOS en próxima sesión usuario
