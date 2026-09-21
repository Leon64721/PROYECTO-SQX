# Ejecución en Vivo: Fix Price Block + Build → OOS — 2026-09-21

**Inicio:** 2026-09-21, [usuario a llenar]

---

## PASO 1: Cierra SQX Completamente

**Usuario debe hacer:**
1. Si SQX está abierto, ciérralo completamente (File → Exit)
2. Espera 5 segundos
3. Confirma que NO hay proceso `StrategyQuantX.exe` corriendo:
   ```
   tasklist | findstr StrategyQuant
   ```
   (Si aparece algo, mata el proceso: `taskkill /IM StrategyQuantX.exe /F`)

**Documenta aquí cuando SQX esté cerrado:** [usuario: timestamp]

---

## PASO 2: Reabre SQX

**Usuario debe hacer:**
1. Abre PowerShell o CMD en `C:\SQX_144_Full`
2. Ejecuta:
   ```
   .\StrategyQuantX.exe
   ```
3. Espera ~30 segundos a que cargue (verás la ventana principal)

**Documenta cuando SQX haya cargado:** [usuario: timestamp]

---

## PASO 3: Abre Proyecto V3_MTF_CLEAN

**Usuario debe hacer:**
1. En SQX → **File → Open**
2. Navega a: `C:\SQX_144_Full\user\projects\NDXm_ORB_PropFirm_V3_MTF_CLEAN`
3. Selecciona: `project.cfx`
4. Click **Open**
5. Espera a que cargue (~10 segundos)

**Verifica:**
- ¿Se carga el proyecto sin errores?
- ¿Ves Build-Task1 llamado "BS-NDXm_ORB_MTF"?
- ¿No hay mensajes de error rojos?

**Documenta:** [usuario: SÍ/NO, cualquier error]

---

## PASO 4: Crear Random Group VALUE

**Usuario debe hacer:**

1. En la ventana principal, busca el panel lateral izquierdo
2. Navega a: **AlgoWizard → Random Groups**
3. Click derecho en el área vacía → **New Group** (o botón "+")
4. Se abrirá un diálogo. Configura:
   - **Name:** `Levels_ORB_NDXm`
   - **Type:** `VALUE` (desplegable, busca "Value" o "price levels")
   - **Category:** `ORB Levels` (opcional)

5. Click **OK**

6. Ahora agrega los items. Click en el grupo recién creado, luego **+ Add Item**:
   - Primer item: `Highest[1]` (prior day high)
   - Segundo item: `Lowest[1]` (prior day low)
   - Tercer item: número constante `100`

**Documenta:** [usuario: grupo creado SÍ/NO, ¿cuántos items?]

---

## PASO 5: Asigna el Grupo al Build-Task1

**Usuario debe hacer:**

1. En la izquierda, selecciona **Build-Task1** (BS-NDXm_ORB_MTF)
2. Abre la pestaña **Genetic Options** o **Building Blocks**
3. Busca donde se asignan "Random groups" o "Value slots"
4. Si ves un desplegable vacío o un slot para VALUE, selecciona **Levels_ORB_NDXm**
5. Guarda

**Nota:** Si no encuentras dónde asignarlo en la UI, es OK — AlgoWizard puede haberlo asignado automáticamente. Continuamos al Paso 6.

**Documenta:** [usuario: asignado SÍ/NO, ubicación en UI]

---

## PASO 6: Guarda el Proyecto

**Usuario debe hacer:**

1. File → **Save** (o Ctrl+S)
2. Verifica que el archivo se guardó (sin errores)

**Documenta:** [usuario: guardado SÍ/NO]

---

## PASO 7: Ejecuta Build → OOS

**Usuario debe hacer:**

1. En la izquierda, selecciona **Build-Task1**
2. Click **Run** (o botón verde de play)
3. Si te pide un nombre, ingresa: `NDXm-MTF-FIX-Build1`
4. Build comienza

**Monitor en vivo:**
- Observa la barra de progreso
- Tiempo esperado: ~30-40 minutos
- Verás "databank is full" cuando termine

**Documenta cada 5 minutos:**
- Hora
- % progreso
- CPU (¿está activo?)

---

## PASO 8: CHECKPOINT OOS

Cuando Build termine, OOS comienza automáticamente.

**Lo más importante:**

Busca en el log esta línea (aproximadamente):
```
[TIME] Retest1 : OOS complete / strategies passed filter / X sobrevivientes
```

o

```
[TIME] [Estadísticas finales] X strategies survived OOS
```

**CHECKPOINT CRÍTICO:**
- **¿Sobrevivientes > 0?**
  - **SÍ ✅** → Ventana ORB FUNCIONA FINALMENTE
  - **NO ❌** → Aumentar umbral de aceptación

**Documenta:** [usuario: sobrevivientes = __/__]

---

## LOGS A MONITOREAR

Archivo: `C:\SQX_144_Full\user\log\StrategyQuant\log_2026_09_21.log`
(o el log del día actual si cambia la fecha)

Busca estas líneas clave:
```
11:XX:XX BS-NDXm_ORB_MTF : Starting Build
11:XX:XX BS-NDXm_ORB_MTF : All backtest data prepared
11:XX:XX BS-NDXm_ORB_MTF : Finished in XXs - Y strategies generated
11:XX:XX Retest1 : Starting OOS
11:XX:XX Retest1 : All backtest data prepared
11:XX:XX Retest1 : OOS complete / [RESULTADOS]
```

---

## TIMELINE ESPERADO

```
[USUARIO INICIA] Cierra/reabre SQX, carga V3
~5 min

[USUARIO EJECUTA] Crea Random Group en AlgoWizard
~5 min

[USUARIO EJECUTA] Guarda proyecto
~1 min

[USUARIO EJECUTA] Build → Run
~30-40 min (MONITOREADO)

[SISTEMA] OOS automático
~30-40 min (MONITOREADO)

[CHECKPOINT] Sobrevivientes > 0?
→ FIN FASE 1
```

**TOTAL: ~1.5 horas**

---

## PRÓXIMOS PASOS (Si sobrevivientes > 0)

- FASE 2: Heredar MTF en Retest-Task2-7
- FASE 3: Ejecutar cadena robustez completa (MC, SPP, WFA)

---

**Estado:** EN PROGRESO
**Responsable:** Usuario en SQX
**Agente:** Monitoreando logs y documentando resultados

---

[USUARIO COMPLETA CADA SECCIÓN ARRIBA]
