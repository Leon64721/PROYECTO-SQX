# Proyecto: StrategyQuant X — Prop Firm / Trading Algorítmico

Esta carpeta contiene el **trabajo del proyecto** (notas, código custom, configuración de
estrategias, gestión de proyecto prop firm, resultados). Es una copia migrada el 2026-08-04 desde
`C:\SQX_144_Full`.

## Inicio de sesión: preguntar en qué frente se va a trabajar

Este proyecto tiene **dos frentes de trabajo distintos y en curso**. Al iniciar una sesión nueva en
esta carpeta, si el primer mensaje del usuario no deja claro de cuál se trata, **preguntar
explícitamente** (por ejemplo con la herramienta de pregunta al usuario) cuál de los dos quiere
trabajar, dando esta breve descripción de cada uno:

1. **Agente de Trading (ML / Qlib→ONNX→SQX)** — desarrollo de una señal/indicador basado en machine
   learning (modelo Qlib exportado a ONNX) integrado como bloque nativo de Builder en SQX
   (`QlibSignal`), para minar y operar estrategias que usan esa señal ML como parte de la lógica de
   entrada/salida. Ver `user\Qlib_ONNX_Bridge_Design.md` y las entradas relacionadas con
   `QlibSignal` en `user\PropFirm_Management\INDEX.md` (ítems 15 y 18).
2. **Generación de Custom Projects SQX (reglas clásicas)** — construcción/parcheo de Custom Projects
   `.cfx` completos (Builder + cadena de robustez: OOS, MC_TRADES, MC_SPREAD_SLIPPAGE, TICK, SPP,
   WFA MATRIX) para un activo/broker específico, usando el paquete de skills
   `SQX_PROJECT_SKILLS_OOS_20_30_EXISTING_SESSION_SHORTNAME_SAFE_20260517\` y el pipeline de costos
   reales vía MT5. Ver `user\PropFirm_Management\INDEX.md` ítem 19 para el caso ya trabajado
   (NDXm_TICK_UTCPlus02).

No asumir cuál de los dos por defecto — son líneas de trabajo independientes con su propio estado,
archivos y próximos pasos.

## Importante: qué NO está aquí

La **aplicación StrategyQuant X instalada** (ejecutables, licencia, motor Java interno, JDK
embebido) y la **caché de datos de mercado/databanks** (`user\data`, ~25GB) se quedaron
intencionalmente en `C:\SQX_144_Full` — no se duplicaron aquí porque:
- La app está en uso activo (procesos corriendo) y su licencia/rutas están atadas a esa ubicación.
- La caché de mercado es regenerable/re-sincronizable y ya hay incidentes previos documentados de
  pérdida de datos al mover databanks.

Esto significa que **cualquier ruta relativa a `internal\`, `j64\`, `user\data\` o `user\log\`
mencionada en las notas de abajo se refiere a `C:\SQX_144_Full`, no a esta carpeta**. Ejemplos:
inspeccionar jars (`internal\libs\SQTradingLib.jar`), usar el JDK embebido (`j64\bin\javac.exe`),
o leer logs en vivo (`user\log\StrategyQuant\...`) — todo eso se hace contra `C:\SQX_144_Full`.

La app sigue corriendo y generando resultados nuevos en `C:\SQX_144_Full\user\projects\...`. Esta
copia en E: es un snapshot al 2026-08-04; **no se sincroniza automáticamente** con lo que la app
siga produciendo en C:. Ver conversación con el usuario sobre estrategia de sincronización.

### Configuración Multi-Temporal ORB (Custom Project)
- **Data 1:** Gráfico principal M15 (Ej. GBPUSD).
- **Data 2:** Gráfico secundario H1 para tendencia.
- **Señales:** ORBLongBreakout y ORBShortBreakout activados (el resto desactivados).
- **Filtros (Confirmación):** Volumen, ATR y SMA/EMA activados para combinarse genéticamente.
- **Money Management:** Salidas con Stop Loss/Take Profit basados en ATR y *Exit at End of Day* habilitado.
- Se ha generado un script automatizado `create_project.py` que inyecta esta configuración en un archivo `ORB_MTF_Project.cfx` importable.

## 4. Problemas de UI - Vistas y DataBanks (Agosto/Septiembre 2026)
- **Error "View with name 'Default - Cloned' doesn't exist"**: Este error emergente NO bloquea ni invalida los datos del `.cfx`. Sucede cuando la tabla del databank (ej. en la matriz de Walk-Forward) tiene seleccionada por defecto en el `.cfx` una vista de columnas que ya no existe en el Workspace o que fue eliminada por el usuario. **Solución**: Hacer clic en el desplegable de "View" de esa sub-tabla y seleccionar `Default - Main data` o `Default - WF`.
- **Filtro Walk-Forward Matrix (WFA)**: El tag `<Conditions thresholdPct="80" robCombRows="2" robCombCols="2" robMinComb="3">` controla el área obligatoria requerida de OOS% vs Runs. Para exigir una matriz 3x3 al 100%, se debe forzar la configuración a `robCombRows="3"`, `robCombCols="3"`, y `robMinComb="9"`.

## Dónde empezar

1. **`user\ClaudeCode_SQX_Notes.md`** — bitácora técnica completa: API real de SQX, jars, cómo
   leer `orders.bin`, caché de columnas, incidentes de crash, etc. Leer la sección "Referencia
   rápida" antes de investigar algo nuevo sobre SQX.
2. **`user\PropFirm_Management\INDEX.md`** — fuente de verdad de qué está hecho/pendiente/pausado
   en el proyecto de cuentas de fondeo (prop firm). Tabla con 14 planes/hallazgos, cada uno con su
   archivo propio.

## Estructura

- `user\extend\` — código custom (Snippets Java, ResultsPlugins Vue/HTML, Plugins, CustomAnalysis)
- `user\projects\` — proyectos y estrategias `.sqx`
- `user\PropFirm_Management\` — planes y decisiones del proyecto prop firm (protocolo: todo cambio
  relevante debe registrarse aquí, no solo mencionarse en las notas)
- `user\settings\` — configuración de usuario de SQX
- `user\_staging_TESTROB_2026-08-02\`, `_staging_TESTROB_DEDUP_2026-08-02\`, `_recovery_2026-08-01\`
  — carpetas de trabajo de sesiones de filtrado/robustez y recuperación de datos
- `user\log\` — copia de logs históricos (los logs en vivo siguen escribiéndose en C:)
- `custom_indicators\`, `VolumeProfile\` — indicadores custom para plataformas externas
- `tests\` — pruebas relacionadas al proyecto

## Convenciones de trabajo (heredadas del proyecto original)

- Después de investigar algo nuevo y estable sobre la API/comportamiento de SQX, añadirlo a la
  sección "Referencia rápida" de `ClaudeCode_SQX_Notes.md` (nunca borrar el historial).
- Todo plan/config/decisión de prop firm debe quedar registrado en `PropFirm_Management\INDEX.md`.
- Verificar en la app real (o su log) antes de dar por hecho que algo quedó guardado/aplicado —
  no asumir.

## GBrain Configuration (configured by /setup-gbrain)
- Mode: local-stdio
- Engine: pglite
- Config file: ~/.gbrain/config.json (mode 0600)
- Setup date: 2026-08-12
- MCP registered: no (Claude Code CLI not on PATH in this environment — register `gbrain serve`
  manually if using the standalone CLI elsewhere)
- Artifacts sync: off
- Transcript ingest: incremental (historical transcripts not bulk-ingested; new sessions tracked
  going forward)
- Current repo policy: n/a (this folder is not a git repository)

## 3. Generación de Custom Blocks (Reglas de Trading en XML)
Desde agosto de 2026, tenemos incorporada la skill **sqx-custom-block**, una herramienta que nos permite traducir ideas de trading en lenguaje natural (o en código como Python/PineScript) directamente a archivos XML nativos de AlgoWizard para StrategyQuant X.
*   **¿Dónde está?:** `01_BIBLIOTECA_CONOCIMIENTO\skills_sqx\SQX_CUSTOM_BLOCKS_SKILL\unzipped\sqx-custom-block`
*   **¿Cómo funciona?:** Ya se ejecutó el proceso de "Bootstrap" contra la instalación de `C:\SQX_144_Full`, por lo que el sistema generó un `catalog.json` y `catalog.md` en esa ruta. Este catálogo conoce todos los indicadores instalados y personalizados del usuario.
*   **Flujo de uso cuando el usuario pide crear una regla:**
    1. Ve a la carpeta de la skill: `cd "E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\01_BIBLIOTECA_CONOCIMIENTO\skills_sqx\SQX_CUSTOM_BLOCKS_SKILL\unzipped\sqx-custom-block"`
    2. Usa el script de Python `examples/gen_example.py` como plantilla base para estructurar las nuevas condiciones (Conditions) o `examples/gen_pricelevel_example.py` para niveles de precios (Price Levels).
    3. Asegúrate de verificar los indicadores disponibles leyendo `catalog.md`.
    4. Genera el bloque con `python <tu_script_generador.py> catalog.json output.xml`.
    5. **Siempre** valida el bloque con: `python engine/validate.py output.xml --catalog catalog.json`.
    6. Entrega el archivo XML final al usuario para que lo importe en **AlgoWizard -> Custom Blocks**.
    7. Este mecanismo evita el repainting, look-ahead bias (shift 0), y errores de código de Java al estructurar las condiciones matemáticamente con base en los bloques autorizados de la máquina del usuario.




## 4. Análisis Experto de Databanks y Filtrado de Correlación (Septiembre 2026)
Se ha implementado un framework automatizado en Python para identificar y aislar las mejores estrategias verdaderamente diversificadas tras su paso por el Walk-Forward Analysis (WFA) u otros databanks:
- **Herramientas base**: `analyze_wfa_databank.py` y `analyze_databank.py` (ubicados en `04_HERRAMIENTAS_SCRIPTS\`).
- **Lectura de memoria detallada**: Ver archivo `04_HERRAMIENTAS_SCRIPTS\PROTOCOL_DATABANK_ANALYSIS.md`.
- **Instrucción al Agente**: Siempre que el usuario solicite "analizar estrategias", "ver databank", "ranking", etc., debes referirte a `PROTOCOL_DATABANK_ANALYSIS.md` y utilizar los scripts en Python generados para procesar el CSV exportado, calcular el Composite Score y ejecutar la lógica de desempaque de `.sqx` para descartar estrategias gemelas (correlacionadas).

## 5. Protocolo de cierre de sesión (obligatorio, automático)

Cuando el usuario pida **cerrar sesión / guardar todo lo hecho** (frases como "cierra sesión",
"guarda todo", "terminemos por hoy", "vamos a cerrar"), el agente debe ejecutar SIEMPRE, sin que
el usuario tenga que pedirlo explícitamente cada vez, estos dos pasos del catálogo de contenido
de `project-organizer` (ver ítem #32 de `user\PropFirm_Management\INDEX.md`) **antes** de dar por
cerrada la sesión:

1. **Escanear lo nuevo**: correr
   `cd ".claude\skills\project-organizer"; python engine\scan_content.py`
   para detectar cualquier Custom Project, portfolio, Custom Block o Random Group nuevo generado
   durante la sesión (queda con `status=pendiente_clasificar`, nunca se adivina el tipo).
2. **Clasificar lo detectado con el usuario**: si `scan_content.py` reporta items nuevos, el
   agente pregunta al usuario (una pregunta a la vez, con `ask_user`) qué `strategy_type`/`status`
   les corresponde — igual que se hizo en la sesión del 2026-09-16 — y los aplica con
   `python engine\classify_content.py "<ruta>" --strategy-type <tipo> --status <estado>`.
   Recordar el criterio de alcance ya acordado: **solo se cataloga lo que resulta de EJECUTAR
   algo** (`02_PROYECTOS_ACTIVOS`, `03_RESULTADOS`, `user\projects`) — material de
   `01_BIBLIOTECA_CONOCIMIENTO` (plantillas, skills descargadas) no se cataloga.
3. Regenerar la vista humana: `python engine\render_catalog.py` (actualiza
   `01_BIBLIOTECA_CONOCIMIENTO\CATALOGO_PROYECTO.md`).
4. Si hubo movimientos de archivos durante la sesión, correr también
   `python engine\validate.py` para confirmar que la estructura de carpetas sigue consistente.

Si `scan_content.py` no detecta nada nuevo (0 items agregados), continuar sin preguntar nada más
— no hace falta interrumpir al usuario si no hay pendientes. Este protocolo no reemplaza el cierre
normal de documentación (actualizar `INDEX.md`/notas de `PropFirm_Management` cuando aplique), es
un paso adicional específico para mantener el catálogo de contenido siempre al día.
