# RunCompare Pre-Flight Checklist — Antes de FASE 1
**Fecha:** 2026-09-21  
**Objetivo:** Verificar que RunCompare está disponible en tu instalación de SQX y listo para FASE 1

---

## PREGUNTA CLAVE

**¿RunCompare ya está descargado, instalado e integrado?**

**Respuesta corta:** RunCompare es **built-in en SQX Build 144+**, NO requiere instalación separada. Solo necesita **verificación** de que:
1. Tu SQX es versión 144+ (sí, confirmado: directorio `C:\SQX_144_Full` → "144")
2. RunCompare está VISIBLE en la UI de SQX

---

## PASO 1: VERIFICAR QUE RUNCOMPARE EXISTE EN TU SQX

### Opción A: Verificación rápida en la UI (RECOMENDADO)
1. **Abre SQX** (StrategyQuantX.exe)
2. Ve a **Tools** (menú superior)
3. ¿Ves **"RunCompare"** en la lista?
   - **SÍ** ✅ → Continúa con PASO 2
   - **NO** ❌ → Sigue PASO 1B (alternativa)

### Opción B: Si NO está en Tools
1. Abre **Help → About** (verifica Build 144+)
2. Si es Build 144+, RunCompare debería estar. Si NO lo ves:
   - **Acción:** Actualiza SQX (Settings → Check for Updates)
   - Reinicia SQX
   - Retorna a PASO 1, Opción A

---

## PASO 2: EXPLORAR RUNCOMPARE (Familiarización)

1. **Tools → RunCompare**
2. Verás una interfaz que muestra:
   - **Historial de Builds:** Lista vacía (es la primera vez, es normal)
   - **Filtros:** Por fecha, databank, proyecto
   - **Botón "New Comparison"** (para comparar 2 builds)
   - **Settings/Preferences** (configuración)

3. **Nota:**
   - Historial estará **VACÍO** hasta que ejecutes Build 1 (FASE 1)
   - RunCompare auto-captura métricas después de cada Build
   - No necesita configuración manual antes de FASE 1

---

## PASO 3: VERIFICAR CONFIGURACIÓN DE TRACKING (OPCIONAL)

**En tu Custom Project NDXm_ORB_PropFirm_V2_MTF_ROBUSTEZ:**

1. Abre el proyecto en SQX
2. Haz clic en **Build-Task1**
3. Mira la sección **"Settings"** → **"Output"**
4. ¿Ves opción **"RunCompare Tracking"** o similar?
   - **SÍ, está habilitado** ✅ → Perfecto, listo para FASE 1
   - **NO está visible** ⚠️ → No importa, RunCompare captura automáticamente de todos modos
   - **Está deshabilitado** ❌ → Habilita (checkbox ON)

**Nota:** SQX 144+ captura automáticamente en RunCompare sin necesidad de configuración manual.

---

## PASO 4: CONFIRMAR QUE BUILDTASK1 TIENE SETTINGS CORRECTOS

Antes de ejecutar FASE 1, revisa que **Build-Task1.xml** tenga:

```xml
<!-- Debe estar presente en tu Build-Task1 -->
<BuildTask name="Build-Task1" ...>
  <StrategyType templateFile="...NDXm_ORB_MTF.sqx">
  <DataBankSettings>
    <OutputDataBank name="BS-NDXm_ORB_MTF" ... />
  </DataBankSettings>
  <!-- RunCompare auto-captura sin necesidad de XML adicional -->
</BuildTask>
```

**Verificación rápida:**
1. Build-Task1 → **Properties**
2. ¿Template = **NDXm_ORB_MTF.sqx**? ✅
3. ¿Output databank = **BS-NDXm_ORB_MTF**? ✅
4. Si ambas sí → Listo para FASE 1

---

## PASO 5: TEST RÁPIDO (OPCIONAL PERO RECOMENDADO)

Para confirmar que todo funciona ANTES de ejecutar FASE 1 completa:

1. **Build-Task1 → Run** pero detén después de **100-200 estrategias** (no esperes las 1800)
2. **Tools → RunCompare**
3. ¿Ves una entrada **"Build 1"** con métricas (PF, Win%, DD%)?
   - **SÍ** ✅ → RunCompare funciona perfectamente
   - **NO** ❌ → Contacta (posible issue raro en versión)

**Nota:** Puedes cancelar este Build de prueba sin problemas. Luego ejecutas FASE 1 completo.

---

## CHECKLIST FINAL (Antes de FASE 1)

```
Pre-requisitos:

☐ SQX 144+ instalado (confirmado: C:\SQX_144_Full)
☐ Tools → RunCompare VISIBLE en la UI
☐ NDXm_ORB_PropFirm_V2_MTF_ROBUSTEZ.cfx cargado
☐ Build-Task1 template = NDXm_ORB_MTF.sqx
☐ Output databank = BS-NDXm_ORB_MTF
☐ (Opcional) Test rápido: 200 estrat. → RunCompare captura

Configuración:
☐ RunCompare Tracking = ENABLED (o auto por defecto)
☐ No hay configuración manual requerida
☐ Histórico de RunCompare = VACÍO (normal, primera vez)

Listo para FASE 1:
☐ Todas las verificaciones arriba = OK
☐ Próximo paso: Build-Task1 → Run (1800 estrategias)
```

---

## TABLA RESUMEN: ESTADO DE RUNCOMPARE EN TU INSTALACIÓN

| Componente | Estado | Verificación | Acción si falta |
|---|---|---|---|
| **SQX Build 144+** | ✅ Confirmado | Carpeta `C:\SQX_144_Full` | N/A |
| **RunCompare en UI** | ? Por verificar | Tools → RunCompare | Si NO: Actualizar SQX |
| **Build-Task1 config** | ? Por verificar | Properties → Template + Output DB | Corregir si mismatch |
| **RunCompare Tracking** | ✅ Auto (default) | Settings → Output | N/A (auto enabled) |
| **Histórico RunCompare** | ✅ Vacío (normal) | Tools → RunCompare | Se llena tras Build 1 |

---

## PRÓXIMOS PASOS

### Si TODO está ✅:
**Ejecuta FASE 1:**
1. Build-Task1 → Run (~1800 estrategias)
2. RunCompare auto-registra "Build 1"
3. Build → Retest → OOS
4. CHECKPOINT: OOS survivors > 0?

### Si ALGO está ❌:
**Contacta / Investiga:**
- RunCompare NO visible → Actualizar SQX Build
- Build-Task1 config mismatch → Corregir template/databank
- Test de 200 estrat. → RunCompare NO captura → Contacta (issue raro)

---

**Estado a 2026-09-21:** Pre-requisitos aún por verificar en UI real de SQX
**Siguiente paso:** Usuario ejecuta PASO 1 (Opción A) arriba
**Tiempo estimado para verificación:** 5 minutos

---

## NOTA IMPORTANTE

**RunCompare NO es "opcional"** en el plan. Es la herramienta central que automatiza:
- Comparación de builds (V1 vs V2 vs V3)
- Selección de estrategias (TOP N ranking)
- Histórico de versiones (nunca pierdes una)

Sin RunCompare, FASE 3-4 requerirían manual labor (Excel, Python scripts).
Con RunCompare, todo es **automático y visual**.

**Es el "hub" que conecta:**
Build 1 (FASE 1) → Build 2 (FASE 2) → Full Chain (FASE 3) → Iteración rápida (FASE 4)
