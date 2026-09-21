# PLAN ESTRUCTURADO: Diagnóstico y Recuperación de Proyectos NDXm V5
**Fecha:** 2026-09-21  
**Estado:** 🔴 PLAN PENDIENTE EJECUCIÓN — NO TOCAR CÓDIGO SIN CONFIRMACIÓN  
**Autor:** Claude Code (Diagnóstico + Plan)

---

## PARTE 1: CONTEXTO Y CONEXIÓN CON "AGENTE DE TRADING" (QlibSignal)

### ¿Cuándo se cruzó "Trading signals" con QlibSignal?

**Timeline de convergencia:**
1. **2026-08-16 (Ítem #18):** QlibSignal registrado en Builder como bloque nativo
   - Aparece como `(QS) Qlib Signal` en Building blocks > Indicators
   - 500 outputs finitos, paridad Java/Python exacta, JNI sintético confirmado
   - **Status:** Disponible para usar en cualquier estrategia

2. **2026-09-16 (Ítem #34):** NDXm_ORB_PropFirm_V2_MTF_ROBUSTEZ generado con sqx-lab chain
   - `Levels_ORB_NDXm` (Value group con 4 price levels)
   - `NDXm_ORB_MTF.sqx` template (M15 Breakout + H1 PropFirmCompliance)
   - **NO menciona QlibSignal en esta versión**

3. **2026-09-17 (Ítem #35 del INDEX):** V3/V4/V5 intentadas, V5 FALLA
   - V5_LONG carga con error: `Cannot create strategy from XML! Error while parsing rule 'Trading signals' - Block doesn't contain item 1`
   - **Hipótesis:** Alguien intentó inyectar QlibSignal en la regla 'Trading signals' pero:
     - El bloque no fue cablear correctamente en el XML
     - O fue referenciado un índice (item 1) que no existe
     - O el Random Group/Custom Block fue deletado entre V2 y V5

### ¿Por qué "Trading signals" ahora?

**Interpretación del error "Block doesn't contain item 1":**
- La regla 'Trading signals' en V5_LONG tiene una estructura que espera múltiples items
- Probablemente intenta usar: `Breakout_Triggers_NDXm` (item 0) + `QlibSignal` (item 1)
- Pero item 1 está **desaparecido** o mal referenciado
- **Síntoma idéntico al ORB V7:** bloque sin cablear → Build falla a los 40 segundos, 70%+ excepciones

---

## PARTE 2: HALLAZGOS TÉCNICOS (No asumidos, verificados)

| Artefacto | Existe en disco | Estado | Observación |
|-----------|-----------------|--------|------------|
| `NDXm_ORB_MTF.sqx` | ✅ (16/09/2026) | Usada por V2 (FUNCIONA) | Template OK, probada |
| `NDXm_ORB_MTF_LONG.sqx` | ✅ (17/09/2026) | Usada por V5_LONG (FALLA) | Template posterior, nunca testeada |
| `NDXm_ORB_MTF_SHORT.sqx` | ❌ NO EXISTE | Error: "file not found" | V5_SHORT proyecto nunca se creó en disco |
| `Levels_ORB_NDXm` Random Group | ✅ En AlgoWizard | V2 usa, importado 16/09 | OK |
| `Breakout_Triggers_NDXm` Random Group | ✅ En AlgoWizard | V2 usa, importado 16/09 | OK |
| `PropFirmComplianceFilters_NDXm` Random Group | ✅ En AlgoWizard | V2 usa, importado 16/09 | OK |
| `QlibSignal` Custom Block | ✅ En Builder (18/08/16) | No usado en V2; ¿usado en V5? | **Aquí está la sospecha** |
| V2 project.cfx | ✅ (380 KB) | Build + OOS completo sin errores | Working baseline |
| V5 project.cfx | ✅ (74 KB) | Build falla a los 40s, 70%+ excepciones | 80% más pequeño = generado automático |

---

## PARTE 3: CAUSA RAÍZ PROBABLE

**Escenario reconstructivo:**

1. **V2 (funciona):** `sqx-strategy-project` clonó correctamente, usó template `NDXm_ORB_MTF.sqx`
2. **V5 intent (falla):** Alguien (usuario o agente) intentó "mejorar" V5 agregando QlibSignal
   - Regeneró template `NDXm_ORB_MTF_LONG.sqx` con QlibSignal inyectado
   - O modificó el Build-Task1.xml para incluir QlibSignal en 'Trading signals'
   - **Pero:** el XML quedó mal estructurado: Random Group referenciado no existe, o índice roto

3. **Verificación necesaria (sin cambiar nada aún):**
   - Descomponer V5_LONG.cfx (es un ZIP)
   - Leer config.xml + Build-Task1.xml
   - Grep por "QlibSignal" o "Trading signals"
   - Comparar estructura vs V2 Build-Task1.xml

---

## PARTE 4: PLAN DE TRABAJO (EN ORDEN, SIN EJECUCIÓN AÚN)

### FASE A: DIAGNÓSTICO (TEXTO + LECTURA, SIN TOCAR CÓDIGO)

**A1.** Extraer ZIP de V5_LONG.cfx y V2.cfx, leer config.xml + Build-Task1.xml
   - Buscar: references a `QlibSignal`, estructuras `<RandomCondition>`, índices en 'Trading signals'
   - Comparar: ¿qué cambió entre V2 (OK) y V5 (falla)?
   - **Salida esperada:** Documento "V5 vs V2 structure diff"

**A2.** Verificar en INDEX.md cuándo exactamente se intentó crear V5
   - ¿Fue usuario o agente externo?
   - ¿Se documentó el intent?
   - **Salida esperada:** Línea de tiempo de quién/cuándo/por qué se creó V5

**A3.** Confirmar si QlibSignal debería estar en V5 o fue un error
   - Leer el cierre de sesión 2026-09-16/17
   - ¿Había un plan de "agregar ML signal a V5"?
   - **Salida esperada:** Decisión: ¿QlibSignal era el plan o fue accidental?

### FASE B: ARCHIVADO DE OBSOLETOS (project-organizer)

**B1.** Marcar V5_SHORT y V5_LONG como obsoletos en el catálogo
   - Comando: `python .claude\skills\project-organizer\engine\classify_content.py "<ruta>" --strategy-type orb_custom_project --status obsoleto_no_recuperable`
   - Razón: "Generado 2026-09-17 con referencia QlibSignal rota; estructura XML incompatible con V2; sobrescrito por opción A (clonar V2)"
   - **Salida esperada:** Entrada en `01_BIBLIOTECA_CONOCIMIENTO\CATALOGO_PROYECTO.md`

**B2.** Regenerar catálogo de contenido
   - Comando: `python .claude\skills\project-organizer\engine\render_catalog.py`
   - **Salida esperada:** Actualizado CATALOGO_PROYECTO.md con V5 marcado como obsoleto

### FASE C: VALIDACIÓN DE OPCIÓN A (CLONAR V2)

**C1.** Copiar V2 como base → `NDXm_ORB_PropFirm_V3_MTF_CLEAN`
   - `cp -r "C:\SQX_144_Full\user\projects\NDXm_ORB_PropFirm_V2_MTF_ROBUSTEZ" "C:\SQX_144_Full\user\projects\NDXm_ORB_PropFirm_V3_MTF_CLEAN"`
   - Actualizar referencias internas de nombre si es necesario (grep + sed)
   - **Salida esperada:** Proyecto nuevo listo en disco

**C2.** Verificación pre-lanzamiento en SQX (UI real, no script)
   - Cerrar/reabre SQX
   - File → Open → NDXm_ORB_PropFirm_V3_MTF_CLEAN
   - Verificar que Build-Task1 carga sin errores XML
   - Verifica que los dos charts (M15 + D1) aparecen en Data Config
   - **Salida esperada:** Pantalla capturada, "Proyecto cargado OK en SQX"

**C3.** FASE 1: Build → Run
   - Build-Task1 → Run (~1800 estrategias)
   - RunCompare auto-registra como "NDXm-MTF-Build1"
   - **Checkpoint crítico:** ¿Build genera 1800 estrategias?
     - **SÍ** → Continúa a C4
     - **NO** → Diagnóstico separa (diferente raíz causa que V5)

**C4.** FASE 1: OOS validation
   - Build → Retest → OOS (primero de 7 tareas)
   - RunCompare captura "OOS-Task1" metrics
   - **Checkpoint CRÍTICO:** ¿OOS produce sobrevivientes > 0?
     - **SÍ** → La ventana ORB anclada a apertura NY real **por fin funciona** ✅ (4 intentos atrás resultó en 0)
     - **NO** → Ajusta umbral DrawdownPct: 35% → 40% o 45% (modo DISCOVERY no ESTRICTO)

### FASE D: DECISIÓN SOBRE QLIB SIGNAL PARA V5 (FUTURO)

**D1.** Si FASE 1-C es exitosa:
   - Documentar: "V2 clone (V3_MTF_CLEAN) está VIGENTE, OOS survivors > 0, ventana ORB CONFIRMADA"
   - Guardar V5_SHORT/V5_LONG como referencia histórica (nunca recuperar, solo diagnóstico)

**D2.** Si usuario quiere agregar QlibSignal posteriormente:
   - Crear V4_WITH_QLIB a partir de V3 Clean (no desde V5 roto)
   - Usar sqx-custom-block para verificar que QlibSignal se importa bien
   - Generar nuevo template NDXm_ORB_MTF_WITH_QLIB.sqx
   - Usar sqx-strategy-project para clonar con nueva template
   - **Pero:** esto es FASE 2+, no bloqueador de FASE 1

---

## PARTE 5: ARCHIVADO Y GOBERNANZA

### Guardar obsoletos (sin borrar)

Todos los artefactos V5 se conservan en:
```
05_ARCHIVO_DESCARTABLE/
└── ndxm_orb_propfirm_v5_diagnostico_2026_09_21/
    ├── NDXm_ORB_PropFirm_V5_LONG_SP500_MTF/   (proyecto entero)
    ├── NDXm_ORB_PropFirm_V5_SHORT_SP500_MTF/  (nunca existió, solo intent)
    ├── DIAGNOSTICO_V5_vs_V2_structure_diff.md (output de FASE A1)
    └── README.md ("Por qué obsoleto, cuándo intentar recuperar")
```

### Protocolo project-organizer

**Regla nueva:** Todo Custom Project obsoleto debe quedar registrado en:
1. `01_BIBLIOTECA_CONOCIMIENTO\CATALOGO_PROYECTO.md` con status=obsoleto
2. `05_ARCHIVO_DESCARTABLE\` con fecha + razón en README
3. `INDEX.md` con link a la sección de diagnóstico (nunca borramos líneas, las archivamos)

**Esto evita:** Volver a intentar lo mismo, perder contexto, olvidar por qué algo falló.

---

## PRÓXIMOS PASOS (CONFIRMACIÓN REQUERIDA)

🟢 **PLAN APROBADO por usuario** → Ejecutar FASE A (diagnóstico puro, sin código)  
🔴 **PLAN RECHAZADO** → Usuario especifica qué cambiar

**Preguntas para el usuario:**

1. ¿Está de acuerdo con archivar V5_SHORT/V5_LONG como "no recuperable"?
2. ¿Confirmamos que la OPCIÓN A (clonar V2 como V3_MTF_CLEAN) es la que quieres validar?
3. ¿Cuál es tu intent con QlibSignal? ¿Lo querías en V5 o fue accidental?

**Timing estimado sin cambios de código:**
- FASE A (diagnóstico): 30 min
- FASE B (archivado): 5 min
- FASE C (validación V3_CLEAN): 2 horas en SQX (Build + OOS)
- **Total semana 1:** Sábado/domingo próximo si ejecutas FASE C

---

**Documento generado:** 2026-09-21  
**Estado:** Pendiente confirmación del usuario antes de ejecutar cualquier FASE
