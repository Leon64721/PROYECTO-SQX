# FASE 1: Build + OOS Validation — Informe en Vivo
**Fecha:** 2026-09-21  
**Proyecto:** NDXm_ORB_PropFirm_V3_MTF_CLEAN  
**Estado:** 🔴 EN PROGRESO

---

## TIMELINE DE EJECUCIÓN

### [PASO 1] Verificación Pre-Lanzamiento ✅

**Verificado:**
- ✅ V3_MTF_CLEAN existe en disco: `C:\SQX_144_Full\user\projects\NDXm_ORB_PropFirm_V3_MTF_CLEAN`
- ✅ project.cfx presente: 380,612 bytes (idéntico a V2)
- ✅ Databanks folder presente
- ✅ Estructura XML verificada (clon exitoso de V2 probado)

**Checklist pre-Build:**
- [ ] SQX cerrada (si estaba abierta)
- [ ] SQX reabierta desde C:\SQX_144_Full
- [ ] Proyecto V3_MTF_CLEAN cargado sin errores XML

---

### [PASO 2] Lanzar SQX y Cargar Proyecto ⏳

**INSTRUCCIONES PARA USUARIO:**

1. **Cierra SQX completamente** (si está abierto):
   - Asegúrate que no hay procesos `StrategyQuantX.exe` corriendo
   - Verificar: `tasklist | findstr StrategyQuant` en PowerShell

2. **Abre SQX desde la instalación real:**
   ```
   C:\SQX_144_Full\StrategyQuantX.exe
   ```
   (O usa start-sq.bat si quieres RunCompare)

3. **Carga el proyecto V3_MTF_CLEAN:**
   - File → Open
   - Navega a: `C:\SQX_144_Full\user\projects\NDXm_ORB_PropFirm_V3_MTF_CLEAN`
   - Selecciona: `project.cfx`

4. **Verifica que cargue sin errores:**
   - ¿Ves Build-Task1 con 2 charts (M15 + D1)?
   - ¿No hay mensajes de error "Block doesn't contain" o "template not found"?
   - ✅ **Si sí:** continúa a [PASO 3]
   - ❌ **Si no:** detente y reporta el error exacto

**Documenta:** Hora de inicio, cualquier advertencia o error visible

---

### [PASO 3] Build-Task1: Run (~1800 estrategias) ⏳

**INSTRUCCIONES:**

1. En SQX, selecciona **Build-Task1**
2. Click en **Run** (o botón verde de ejecución)
3. Asigna nombre a la estrategia: **`NDXm-MTF-V3-Build1`**
   - (importante para RunCompare: cada Build debe tener nombre único)

**MONITOREO EN VIVO:**
- Observa la barra de progreso en la ventana de Build
- **Tiempo esperado:** ~30-40 minutos (1800 estrategias)
- **Generación paralela:** Ver núcleos de CPU en uso

**CHECKPOINT BUILD:**
- ✅ **Éxito:** Build termina, "databank is full" o similar
- ❌ **Fallo:** Error después de N segundos, "Grid stopping, job failures exceeded X%"

**Documenta:**
- Hora de inicio exacta
- Línea del log donde termina Build
- Número de estrategias generadas (debe ser ~1800)
- Tiempo total

---

### [PASO 4] Build → Retest (OOS) ⏳

**DESPUÉS que Build termina:**

1. Automáticamente inicia **Retest-Task1** (OOS)
2. Verás en log: "All backtest data prepared"
3. OOS comienza a correr (CPU alta, ~20-40 min)

**CHECKPOINT OOS (CRÍTICO):**

**Durante OOS:**
- Monitorea: `C:\SQX_144_Full\user\log\StrategyQuant\log_2026_09_21.log` (o log del día actual)
- Busca línea: **"strategies passed OOS filter"** o similar
- Anota el NÚMERO de sobrevivientes

**CHECKPOINT DECISIVO:**
```
¿Sobrevivientes OOS > 0?
├─ SÍ (>0) ✅  → Ventana ORB FUNCIONA FINALMENTE
│                Continúa con FASE 2 (heredar MTF)
│                
└─ NO (=0) ❌  → Ventana aún no funciona
               Ajusta umbral: DrawdownPct 35% → 40%
               Repite Build+OOS
```

**Documenta:**
- Hora de inicio de OOS
- "All backtest data prepared" timestamp
- Sobrevivientes: [X de 1800]
- Líneas relevantes del log (Failed details, %)

---

## SECCIONES A COMPLETAR CONFORME SE EJECUTE

### Ejecución Real

**HORA: [usuario inicia aquí]**

```
TIMESTAMP: 
SQX Status: 
Project Loaded: 
Build-Task1 Status: 
Build Start Time: 
Strategies Generated: 
Build End Time: 
OOS Start Time: 
OOS Status: 
Sobrevivientes OOS: 
```

---

## RESULTADOS ESPERADOS POR ESCENARIO

### Escenario A: ✅ OOS Sobrevivientes > 0 (ÉXITO)

**Evidencia de éxito:**
- Build generó ~1800 estrategias sin 70%+ excepciones
- OOS ejecutó sin bloqueos
- OOS reporta N > 0 sobrevivientes

**Interpretación:**
- Ventana ORB anclada a apertura NY real **FINALMENTE FUNCIONA**
- Esto valida que V2 → V3 fue el camino correcto
- 4 intentos fallidos (09-02, 09-06, 09-09, 09-11) se debían a V5 corrupto, NO a la ventana

**Próximo paso:**
- FASE 2: Heredar MTF en Retest-Task2-7
- FASE 3: Ejecutar cadena robustez completa (MC, SPP, WFA)

---

### Escenario B: ❌ OOS Sobrevivientes = 0 (FALLO, revisar umbral)

**Evidencia de fallo:**
- Build OK (~1800 estrategias)
- OOS ejecutó
- OOS reporta 0 sobrevivientes (100% rechazado)

**Diagnóstico (en orden):**
1. Verificar umbral de OOS en XML: ¿DrawdownPct < 35%?
2. Revisar "Failed details" en log: ¿qué % de rechazo? (Drawdown / Trades / otras razones)
3. Si DrawdownPct es el culpable: ajustar a 40-45% (modo DISCOVERY)
4. Re-ejecutar Build+OOS con nuevo umbral

**Próximo paso:**
- Crear Build-Task2 (copia de Task1 con umbral ajustado)
- Ejecutar Build-Task2

---

### Escenario C: ❌ Build falla con excepción (ERROR TÉCNICO)

**Evidencia:**
- Build se detiene a los ~40 segundos
- Grid stopping message
- Error: "Block doesn't contain item X" u otro

**Acción Inmediata:**
- Capturar log exacto del error
- Comparar V3 project.cfx vs V2 byte-a-byte
- Si son idénticos pero falla diferente: problema de SQX app (uptime, memoria, etc.)
- Reiniciar SQX y reintentar

---

## DOCUMENTACIÓN EN VIVO

### Build Execution Log
```
[COMPLETAR DURANTE LA EJECUCIÓN]

Start Time: 
SQX Version: 
Project: NDXm_ORB_PropFirm_V3_MTF_CLEAN
Build-Task1 Status: [Running / Completed / Failed]

Progress:
- [Time] Starting Build
- [Time] Building: X% complete
- [Time] Build Complete - Y strategies generated
- [Time] OOS Starting
- [Time] OOS: All backtest data prepared
- [Time] OOS: [Z% complete]
- [Time] OOS Complete

Results:
- Build Strategies: 
- OOS Passed: 
- OOS Failed: 
- OOS Pass Rate: %
```

---

## CHECKPOINT CRÍTICO

**Al terminar OOS, responde ESTO EXACTAMENTE:**

```
¿Cuántos sobrevivientes de OOS?
[0 = Fallo, >0 = Éxito]

Línea del log donde se reporta (busca "strategies passed"):
[Copia la línea exacta]

Errores vistos durante Build o OOS:
[Sí / No, cuál]

Duración total Build + OOS:
[Horas:Minutos]

¿Ejecutar FASE 2 (heredar MTF) o revisar umbral?
[Basado en sobrevivientes]
```

---

## SIGUIENTE FASE (FASE 2)

**Si OOS Sobrevivientes > 0:**
- Copiar `<RulesComplexity>` + `<RetestOnAdditionalMarkets>` de Build-Task1
- Pegar en Retest-Task1-7 para heredar MTF
- Ejecutar Build-Task2 (validación de mejora vs V3 Build1)
- RunCompare lado-a-lado comparison

**Si OOS Sobrevivientes = 0:**
- Crear Build-Task2 (ajustar umbral DrawdownPct)
- Reintentar Build+OOS

---

## CONTROL DE PROGRESO

| Paso | Descripción | Status | Hora Inicio | Hora Fin | Duración | Notas |
|------|-------------|--------|-------------|----------|----------|-------|
| 1 | Pre-launch verificación | ✅ | — | — | — | V3 listo en disco |
| 2 | Cargar V3 en SQX | ⏳ | — | — | — | Esperando usuario |
| 3 | Build-Task1 Run | ⏳ | — | — | — | Esperando usuario |
| 4 | OOS Validation | ⏳ | — | — | — | CHECKPOINT CRÍTICO |
| 5 | Decisión FASE 2 | ⏳ | — | — | — | Basado en resultados |

---

**Documento vivo:** Se actualiza conforme se ejecuta cada paso  
**Responsable documentación:** Usuario captura timestamps + resultados  
**Validación:** Sobrevivientes OOS decide próximo paso  
**Deadline:** Próximas 4-6 horas de tiempo de máquina (Build ~30-40 min, OOS ~30-40 min)

---

**INICIAR FASE 1 YA** ➜ Sigue instrucciones en [PASO 2] arriba
