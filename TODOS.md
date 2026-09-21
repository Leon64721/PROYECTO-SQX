# TODOS.md

Generado por `/plan-ceo-review` (Fase 2b, 2026-08-12), revisión del flujo Qlib→ONNX→SQX.

## PARCIALMENTE RESUELTO — Auditoría profunda de PropFirmComplianceLogic/NewsCalendar (2026-08-12): 2 de 3 bugs corregidos y desplegados, rollover sigue abierto

**Contexto**: `/review` pidió auditar zonas horarias, regla de consistencia y ventana de noticias en
`PropFirmComplianceLogic.java`/`NewsCalendar.java`/`PropFirm_Apex_*.java`, y activar
`newsRestrictionActive=true` SI la lógica resultaba 100% correcta. No lo es — la condición no se
cumplió, así que NO se activó el flag. De los 3 bugs encontrados, 2 (consistencia + robustez del
CSV de noticias) se corrigieron y desplegaron a `C:\SQX_144_Full` más tarde en la misma sesión (ver
"Qué se hizo" más abajo); el rollover sigue sin corregir. Resumen de los 3 hallazgos:

1. **SIGUE ABIERTO — Rollover/zona horaria (P1, confianza 9/10)**: `computeDailyStatsFromOrders()` y
   `bestDayProfitShare()` agrupan por día con `Order.CloseTime / MILLIS_PER_DAY` — esto es
   medianoche UTC cruda, NO el rollover real de la cuenta prop firm (ej. Apex EOD trailing resetea
   ~17:00-18:00 ET/CT, no medianoche UTC). Afecta drawdownScore, dllScore Y consistencyScore por
   igual (los tres sub-scores comparten el mismo bucketing). No existe ningún parámetro de offset de
   rollover en el código — es una brecha arquitectónica, no un typo.
2. **CORREGIDO Y DESPLEGADO 2026-08-12 — Consistencia usa `Order.PL` en vez de delta de `Order.AccountBalance` (P1, confianza 9/10)**:
   `bestDayProfitShare()` suma `Order.PL` directamente. El propio javadoc de la clase (y
   `ClaudeCode_SQX_Notes.md` líneas 234-237) documenta que esto es exactamente lo que se dejó de
   hacer en drawdown/DLL porque `Order.PL` sumado a mano NO coincide con cómo SQX aplica
   comisión/swap al balance real — por eso ahí se usa `Order.AccountBalance`. La consistencia nunca
   recibió ese mismo fix. El manejo de denominador <=0 (`totalPL<=0` → NaN) SÍ está bien hecho.
3. **CORREGIDO Y DESPLEGADO 2026-08-12 — `NewsCalendar.loadEvents()` no es robusto a CSV malformado (P1, confianza 8/10)**: el parseo
   (`parts[1]`, `LocalDate.parse(date)`) puede lanzar `ArrayIndexOutOfBoundsException`/
   `DateTimeParseException`, ninguna de las dos es `IOException` (el único catch que existe). Una
   fila mal formada en `economic_events_calendar.csv` no queda "fail closed" como dice el comentario
   — se propaga sin capturar, y como `cachedEvents` solo se asigna DESPUÉS del loop, el fallo
   tampoco queda cacheado: cada llamada futura a `countViolations()` reintenta parsear el CSV entero
   y vuelve a lanzar la misma excepción, en cada orden, de cada estrategia, en toda la búsqueda
   genética.

Hallazgo menor CORREGIDO junto con el fix #3: el javadoc de `NewsCalendar.java` decía "TIMEZONE
STATUS: still UNVERIFIED" pese a que `PropFirm_Management/11_capa2_restriccion_noticias.md` ya
documentaba la confirmación empírica del 2026-07-29 — actualizado para reflejar el estado real.

**Qué se hizo (2026-08-12)**: bugs #2 y #3 corregidos, compilados limpio standalone contra
`j64\bin\javac.exe` (los archivos que dependen de `SettingsMap` — las subclases `PropFirm_*.java`
que llaman a `PropFirmComplianceLogic.compute()` — solo compilan dentro del Code Editor real, no
standalone; esto es la limitación preexistente ya documentada, no algo nuevo). Copiados a
`C:\SQX_144_Full\user\extend\Snippets\SQ\Columns\Databanks\`, verificado `diff` idéntico. Sigue
pendiente confirmar dentro del Code Editor GUI real (no solo `javac.exe` en terminal) — mismo
sub-punto abierto que el fix de Log en `OnnxModelManager`/`QlibSignal`.

**Sigue abierto**: bug #1 (rollover) — bloquea activar `newsRestrictionActive` (ítem 11 de
`PropFirm_Management/INDEX.md`) y sigue afectando la precisión real de drawdownScore/dllScore/
consistencyScore para TODOS los perfiles `PropFirm_*` ya en uso, no solo TPT_PRO_Funded.
**Depende de**: decisión del usuario sobre cómo modelar el rollover real de cada prop firm (falta un
parámetro de offset de sesión por perfil, no existe hoy) antes de poder corregir el bug #1.

## RESUELTO — `com.strategyquant.tradinglib.Log` no existe en esta instalación, confirmado en el Code Editor real (2026-08-13)

**Qué pasó**: `OnnxModelManager.java`/`QlibSignal.java` se cambiaron a `Log.error(...)` en la
Tarea T4/T5, con la hipótesis (documentada como tal, no como hecho confirmado) de que SQX
inyectaría `Log` internamente al compilar dentro de su propio Code Editor, mismo patrón ya
documentado para `SettingsMap`/`IXMLAble`/`ISQCloneable`. Al compilar de verdad en el Code Editor
real, dio **"cannot find symbol: Log"** — la hipótesis era incorrecta específicamente para `Log`
(no todos los tipos "faltantes" se inyectan igual; no asumir que el patrón se generaliza).

**Fix aplicado**: revertido a `System.err.println(...)` en ambos archivos, tanto en
`E:\...\STRATEGY QUANT\user\extend\Snippets\...` como en la instalación viva
`C:\SQX_144_Full\user\extend\Snippets\...` (copiados idénticos, verificado con `diff`).
Recompilado limpio contra `javac.exe` embebido apuntando a los archivos reales de
`C:\SQX_144_Full`. Gate de valores dorados re-verificado — sigue exacto tras el revert.

**Sigue pendiente**: confirmar dentro del Code Editor GUI real (no solo `javac.exe` en terminal)
que compila sin errores — sub-punto de classloader de snippets, ver más abajo.

## P0 — Agregar `--enable-native-access=ALL-UNNAMED` a los flags de arranque de SQX — YA RESUELTO, sin que nadie lo agregara (corregido 2026-08-13)

**CORRECCIÓN**: este ítem se creó el 2026-08-12 asumiendo (sin verificar el archivo real en ese
momento) que el flag faltaba. Al releer `C:\SQX_144_Full\CodeEditor.config` y
`StrategyQuantX.config` directamente el 2026-08-13, **ambos archivos YA TENÍAN**
`option --enable-native-access=ALL-UNNAMED` (línea 5 en ambos) — probablemente desde la
instalación original de SQX 1.44, no algo que este proyecto haya agregado. **No se necesita
ninguna edición.**

Esto también explica un hallazgo previo: los warnings de JEP 472 vistos durante el spike P1 y
`GoldenValueTest.java` ocurrieron porque esas pruebas invocaron `java.exe` directo con flags
propios, sin pasar por `CodeEditor.exe`/`StrategyQuantX.exe` (que sí leen estos `.config` y ya
incluyen el flag) — es decir, esos warnings fueron un artefacto del arnés de prueba standalone,
nunca hubieran aparecido en el uso real de SQX vía sus lanzadores reales.

**Lección para la próxima vez**: verificar el archivo real ANTES de escribir "falta X" en
`TODOS.md`, no asumir a partir de un hallazgo de una prueba aislada.

**Esfuerzo**: S (2 líneas, ~2 min).
**Prioridad**: P0 al momento del despliegue real — no bloquea nada del desarrollo/pruebas
actuales (que corren fuera de SQX, en `spike/`, sin este flag, aceptando el warning).
**Depende de**: nada técnicamente, pero solo tiene sentido aplicarlo junto con el resto del
despliegue de Fase 3 (`spike\deploy_to_sqx.ps1`).

## RESUELTO — Compilación externa limpia de snippets Java usando el classpath completo de SQX (2026-08-16)

**Qué pasó**: la compilación de verificación externa se estaba realizando contra una lista parcial
de JARs y no contra el árbol completo de dependencias de la instalación real. Eso dejaba el
resultado expuesto a falsos negativos de `cannot find symbol` o `package ... does not exist`,
particularmente cuando la dependencia venía de `internal\libs\` pero no estaba incluida en la
cadena de classpath del comando de compilación.

**Causa raíz confirmada**: la instancia real de SQX incluye 85 JARs bajo
`C:\SQX_144_Full\internal\libs\` + `C:\SQX_144_Full\user\libs\`; al concatenarlos en un único
classpath dinámico y compilar los snippets Java del directorio
`C:\SQX_144_Full\user\extend\Snippets\SQ\Indicators\` con `javac.exe`, la verificación pasa sin
errores de dependencia. El problema no era un BOM ni un fallo de import, sino una selección
incompleta de jars en la línea de comando.

**Verificación ejecutada**:
- `Get-ChildItem C:\SQX_144_Full\internal\libs\*.jar` + `C:\SQX_144_Full\user\libs\*.jar`
- Construcción de `-cp` con todos los JARs ordenados y únicos
- Compilación con `C:\SQX_144_Full\j64\bin\javac.exe` sobre los 3 archivos reales del árbol
  `SQ\Indicators\` (QlibSignal.java, QlibSignalCore.java, OnnxModelManager.java)
- Resultado verificado: `COMPILE_OK_ROOT_ONLY` / `EXIT:0`

**Conclusión operacional**: se puede avanzar a la fase `/ship` con la auditoría de dependencias
cerrada, siempre usando el árbol completo de JARs de SQX como classpath base para compiling fuera
del editor. El parámetro crítico es incluir el árbol completo de `internal\libs\*.jar` y
`user\libs\*.jar` antes de compilar cualquier snippet de extensión.

**Impacto**: elimina la condición que generaba errores del tipo `SettingsMap` o `package
com.strategyquant.lib does not exist` por dependencia faltante, sin necesidad de tocar la lógica del
snippet ni de la API de SQX.

## P1 — Verificar compatibilidad onnxruntime-java + JDK embebido de SQX (spike) — RESUELTO 2026-08-12

**Resultado**: `com.microsoft.onnxruntime:onnxruntime:1.29.0` **carga correctamente** bajo el JDK
embebido real de SQX (OpenJDK 25.0.1 LTS, Zulu, Windows amd64) — verificado con
`spike/OnnxSmokeTest.java`, compilado y ejecutado directo contra `j64\bin\javac.exe`/`java.exe`.
El jar bundlea nativos `win-x64` (`onnxruntime.dll`, `onnxruntime4j_jni.dll`), confirmados
presentes dentro del jar.

- **JEP 472 SÍ dispara** (confirmado empíricamente, no especulación): sin flags, aparece
  `WARNING: Restricted methods will be blocked in a future release unless native access is
  enabled`. **Se resuelve limpio** agregando `--enable-native-access=ALL-UNNAMED` — mismo
  mecanismo de flags JVM que ya usa `CodeEditor.config`/`StrategyQuantX.config` (ver
  `SQX_Architecture_Notes.md`), un cambio de una línea cuando se despliegue de verdad.
  **No es un bloqueo duro hoy**, solo un warning — pero agregar el flag desde ahora evita que
  una futura actualización de JDK convierta esto en un fallo silencioso.

- **HALLAZGO NUEVO, no relacionado con JDK25/JNI**: `OrtEnvironment.getEnvironment()` tarda
  **38-59 segundos** consistentemente (2 corridas sin flag: 38.7s, 52s; 1 corrida con
  `--enable-native-access`: 59s — el flag no afecta esta latencia, confirmando que es un
  problema separado). Aislado experimentalmente a la capa Java/ONNX Runtime específicamente:
  - JVM bare startup: 0.16s (no es problema de JDK).
  - Copia de archivo E:→C:\Temp (mismo path que la extracción JNI): 0.06s (no es disco).
  - Windows Defender real-time protection: **desactivado** en esta máquina (no es AV).
  - `LoadLibrary` directo del mismo DLL vía PowerShell/kernel32 (sin JVM de por medio):
    **0.066 segundos** (no es el DLL ni el SO — la carga del sistema operativo es instantánea).
  - Verificación de firma Authenticode del DLL: válida, 0.13s (no es eso tampoco).
  - **Conclusión**: el retraso está 100% aislado a la inicialización propia de ONNX Runtime
    Java (`OrtEnvironment`), no a JDK 25 ni a esta instalación de SQX. Causa más probable
    (no confirmada, es la hipótesis más consistente con el patrón observado): enumeración de
    execution providers (GPU/DirectML/CUDA) colgándose al buscar un adaptador de video real —
    comportamiento documentado de ONNX Runtime en VMs/sesiones RDP sin GPU/display real.
  - **Implicación de diseño**: el diseño ya asume "costo único al primer uso, cacheado
    después" (`OnnxModelManager`, sesión compartida) — esta latencia es tolerable bajo ese
    diseño (una vez por sesión de SQX, no por estrategia), pero 40-60s es suficiente para que
    un usuario piense que SQX se colgó. Debe documentarse como comportamiento esperado, no
    como un bug, cuando se implemente de verdad.
  - **Nuevo TODO derivado** (no bloqueante, ver abajo): probar si limitar
    `SessionOptions` a solo `CPUExecutionProvider` explícito evita la enumeración de
    providers y resuelve la latencia — fix común documentado para este patrón.

## P1b — Investigar la latencia de 40-60s en OrtEnvironment.getEnvironment() (nuevo, derivado del spike P1)

**Qué**: probar si forzar `SessionOptions` a usar solo `CPUExecutionProvider` (sin dejar que
ONNX Runtime enumere providers GPU disponibles) elimina la latencia de 38-59s observada.
**Por qué**: aunque es un costo único por sesión de SQX (tolerable según el diseño actual), 40-60
segundos es sospechosamente largo y podría degradarse más en la máquina de producción real
(esta prueba corrió en el entorno de desarrollo, no confirmado si es la misma máquina/VM donde
correrá SQX en producción).
**Contexto**: hallazgo del spike P1 (`TODOS.md`, 2026-08-12) — aislado experimentalmente a la
capa ONNX Runtime Java, descartado JDK/disco/AV/firma/carga de SO.
**Esfuerzo**: S (probar `SessionOptions.addCPU(true)` o equivalente, ~15 min).
**Prioridad**: P3 — no bloquea T1-T5 de `Qlib_ONNX_Bridge_Design.md`, es una optimización.
**Estado**: la implementación de `addCPU(true)` ya quedó aplicada en `OnnxModelManager`; falta
benchmark/corroboración real del efecto en tiempo de carga.

### Sub-puntos de P1 que el spike NO cubrió (deliberadamente fuera de alcance, siguen abiertos)

El spike de arriba probó JDK25/JNI de forma aislada (fuera del classloader de SQX, sin el modelo
real) — dos preguntas relacionadas de la revisión "outside voice" siguen sin verificar:

1. **Interacción con el classloader custom de snippets de SQX**: el jar de ONNX Runtime extrae su
   DLL nativa a un directorio temporal vía `System.load()`. SQX compila/carga snippets de usuario
   mediante su propio classloader custom (no un classpath de app estándar) — si esa extracción
   funciona igual bajo el loader de snippets de SQX, incluyendo permisos de filesystem y el
   comportamiento de hot-reload ya documentado (`ClaudeCode_SQX_Notes.md`), no está confirmado.
   Este es exactamente el tipo de interacción que causó el crash de arranque documentado del
   2026-07-27. **Solo se puede verificar de verdad dentro del Code Editor real de SQX** (Tarea T2
   de `Qlib_ONNX_Bridge_Design.md`), no con un spike standalone.
2. **Throughput/concurrencia**: si SQX paraleliza backtests entre threads durante la búsqueda
   genética, una sola `OrtSession` compartida (requisito ya aprobado) se vuelve un punto de
   contención compartido. Sin medir si `Run()` concurrente escala a la escala real de este proyecto
   (6600+ estrategias en una databank).

**Prioridad de ambos**: P1 — bloquean el uso real en producción, aunque ya no bloquean continuar
con la Tarea T2 (implementar el skeleton), que es precisamente donde se pueden verificar.

---

## P2 — Construir Approach B: pipeline versionado con doble gate out-of-sample

**Qué**: pipeline versionado con manifest (qué archivo `.onnx`, entrenado con qué ventana de datos,
cuándo) + doble validación out-of-sample: gate propio de Qlib (walk-forward, no split aleatorio) Y el
`RobustnessFilter`/staging `TESTROB` que ya existe en este proyecto, antes de promover cualquier
artefacto `.onnx` a "producción".

**Flujo propuesto**:
1. Guardar cada export en un directorio versionado (`models/<yyyy-mm-dd_hhmm>/`).
2. Escribir un `manifest.json` con hash del spec, ventana de entrenamiento, fecha de entrenamiento,
   lista de features, versión del motor y estado de validación.
3. Correr primero el gate propio de Qlib (walk-forward / no leakage).
4. Correr después el gate SQX en `TESTROB` sobre el mismo artefacto congelado.
5. Solo si ambos gates pasan, promover la versión a la ruta activa que consume SQX.
6. Si un gate falla, conservar la versión como histórica pero no promocionarla.
7. Mantener rollback trivial: re-apuntar la ruta activa al último manifest aprobado.

**Por qué**: es el único camino que satisface "pipeline mantenible" a largo plazo — Approach A
(elegido hoy) es deliberadamente el primer paso mínimo, no la arquitectura final. Sin esto, el modelo
se congela sin manera sistemática de saber si sigue siendo válido ni de revertir a una versión
anterior conocida.

**Contexto**: Approach A fue elegido explícitamente sobre Approach B en la revisión CEO del
2026-08-12 (decisión D1) para de-riesgar primero. Esto es lo que viene después si el primer modelo
demuestra valor real.

**Esfuerzo**: L (humano) → M con CC+gstack.
**Prioridad**: P2 — no bloquea el primer resultado, pero es la brecha más importante a mediano plazo.
**Depende de**: que Approach A produzca al menos una señal que el motor genético de SQX use de verdad
(ver también el gate de valor predictivo, hallazgo #9 de la revisión "outside voice" — un chequeo
barato de correlación señal↔retornos futuros en Python, ANTES de invertir en más ingeniería, que no
se hizo todavía y debería preceder incluso a este ítem).

---

## P3 — Definir cadencia de reentrenamiento y reemplazo del modelo en producción

**Qué**: definir cadencia de reentrenamiento del modelo Qlib (ej. mensual, trimestral, o manual bajo
demanda) y cómo se reemplaza el `.onnx` en producción sin romper estrategias que ya lo usan
(monitoreo de decaimiento de la señal incluido — el `RobustnessFilter` valida estructura de
estrategia, no salud de una señal caja-negra específica).

**Decisión registrada**: cadencia **híbrida mensual + disparador por drift**. El modelo se
reentrenará en una ventana fija mensual y también podrá adelantarse si el monitoreo detecta drift
material de la señal o degradación del gate de valores.

**Por qué**: sin esto, el modelo se vuelve obsoleto silenciosamente — nadie sabrá cuándo la señal dejó
de ser válida. Para cuentas de prop firm con límites de drawdown duros, una señal opaca que decae en
silencio es un riesgo de cola más difícil de diagnosticar que el decaimiento de un indicador
interpretable.

**Contexto**: explícitamente diferido al elegir Approach A; depende parcialmente del ítem P2 (Approach
B) pero es una decisión más pequeña y aislada — puede resolverse manualmente sin todo el versionado.

**Esfuerzo**: S/M.
**Prioridad**: P3 — no urge hasta que el primer modelo lleve unas semanas en uso.
**Depende de**: tener un primer modelo funcionando (Approach A).

---

## P4 — Menú gráfico unificado del proyecto (hub SQX)

**Qué**: construir un hub visual en HTML dentro de SQX para navegar y ejecutar los frentes del
proyecto sin depender de terminal: Agente de Trading (Qlib→ONNX→SQX), Custom Projects SQX,
AlgoWizard/custom blocks, consulta de databanks e instrumentos, y accesos a utilidades del flujo.

**Decisión de arquitectura**: la base debe ser un **ResultsPlugin HTML** (no un `index.html`
standalone). Motivo: el plugin vive dentro de SQX, recibe `postMessage`, puede leer contexto de
estrategia/databank y convertirse en una UI dinámica real. Un `index.html` suelto solo serviría como
portal externo, pero no como centro operativo conectado a datos de SQX.

**Objetivo de diseño**: que el menú sea el punto de entrada para crear, inspeccionar y lanzar
workflows de forma gráfica, y que más adelante pueda crecer hacia un panel completo del proyecto.

**Prototipo creado**: `[user/extend/ResultsPlugins/ProjectHub/index.html](E:/PROYECTOS/CLAUDE%20CODE/STRATEGY%20QUANT/user/extend/ResultsPlugins/ProjectHub/index.html)` como base del hub.

**Prioridad**: P2 — infraestructura transversal que simplifica todo el resto del trabajo.
**Depende de**: definir primero los módulos/acciones que el menú debe exponer.

---

## Sesión de Trabajo (2026-09-02)

**Objetivo de la sesión**: Generar 4 archivos CFX específicos para NDXm_TICK_UTCPlus02 (Tickmill) resolviendo todos los placeholders, ejecutando el script `patch_for_master.py`.

**Estado al inicio de la sesión**:
- El script `patch_for_master.py` con las modificaciones necesarias (rutas correctas, definiciones de CFX base, lógica de descompresión Y uso de `UNZIPPED_BASE_DIR` en `process_edge`) estaba finalizado en memoria.
- El archivo `E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\patch_for_master.py` había sido vaciado.

**Acciones realizadas durante la sesión**:
1.  Se intentó escribir el script `patch_for_master.py` en el disco.
2.  Se segmentó el script en 7 fragmentos para intentar superar el límite de caracteres del `editor` tool (6000 caracteres por `new_text`).
3.  Se intentó escribir el "Fragmento 1" del script.

**Problemas encontrados**:
- La herramienta `editor` persiste en su limitación de 6000 caracteres por el parámetro `new_text`. A pesar de la segmentación planificada, el primer intento de escritura de un chunk no se realizó correctamente, y el archivo `patch_for_master.py` permaneció vacío o casi vacío después de la operación.
- `read_files` Y `run_commands` (PowerShell `Get-Content`) han demostrado ser poco fiables para obtener el contenido completo de archivos grandes debido a truncamiento o problemas de caché, lo que dificulta la verificación del estado del archivo Y el cálculo preciso del `insert_line` para operaciones incrementales.

**Estado actual al cierre de la sesión (2026-09-02)**:
- El script `patch_for_master.py` no ha podido ser escrito completamente en el disco.
- La segmentación en chunks debe ser aún más conservadora, Y la estrategia de verificación debe ser reconsiderada para asegurar la escritura exitosa.

**Próximos pasos pendientes (para la reanudación)**:
1.  **Limpiar el archivo `patch_for_master.py`** (si no está ya vacío) para asegurar un punto de partida limpio.
2.  **Re-segmentar el script completo** en aproximadamente **10-15 chunks** (o más, si es necesario), asegurando que cada `new_text` sea **máximo 2000-3000 caracteres** para evitar cualquier límite de la herramienta.
3.  **Escribir cada chunk secuencialmente** en `patch_for_master.py` utilizando `editor` con `insert_line` Y llevando un **seguimiento manual Y estricto** del número de línea para el siguiente `insert_line`.
4.  **Verificar la integridad del archivo**: Después de escribir todos los chunks, intentar leer las primeras Y últimas 50 líneas del archivo con un método confiable (si es posible, si no, se asumirá la escritura basada en el éxito de `editor` calls) para confirmar que el archivo es completo Y preciso en el disco.
5.  **Ejecutar el script**: `python E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\patch_for_master.py` desde la línea de comandos.
6.  **Validar la salida**:
    *   Verificar la creación de 4 archivos `.cfx` en `E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\patched_master_projects\` (ej., `NDXM_TMILL_E1_H1TF_V4.cfx`) con los shortnames correctos.
    *   Confirmar que `calc_summary.json` se generó correctamente.
7.  **Cargar Y probar en SQX**: Cargar los archivos `.cfx` generados en StrategyQuant X Y confirmar:
    *   Todos los placeholders internos están resueltos.
    *   Los gráficos de múltiples marcos de tiempo están configurados correctamente.
    *   Todos los recursos (datos, símbolos, etc.) se vinculan como se esperaba.

**Archivos involucrados**:
- **Origen (en memoria)**: El script Python completo Y modificado para `patch_for_master.py`.
- **Destino**: `E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\patch_for_master.py` (a ser escrito en chunks).
- **Entrada CFX base**: `E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\07_BASE_CUSTOM_PROJECT_MASTER_CLEAN_SQX_V1_SOURCE_ONLY_FIXED.cfx`.
- **Salida**: `E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\patched_master_projects\` (4 archivos CFX de edge + `calc_summary.json`).