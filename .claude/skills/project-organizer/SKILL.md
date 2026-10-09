---
name: project-organizer
description: Mantiene ordenada la carpeta raiz del proyecto "STRATEGY QUANT" clasificando cada archivo/carpeta nueva en una de 5 categorias fijas (biblioteca de conocimiento, proyectos activos, resultados, herramientas/scripts, archivo descartable), sin nunca tocar user\ ni borrar nada. Tambien mantiene un catalogo de CONTENIDO (que tipo de estrategia es cada Custom Project/portfolio/bloque, y si sigue vigente u obsoleto), separado de la ubicacion fisica. Usar cuando el usuario descargue material nuevo de biblioteca SQX, cree un script o carpeta suelta en la raiz, pida "ordenar el proyecto", "revisar si algo quedo suelto", "clasificar esto que acabo de descargar", o pida inventariar/clasificar que tipo de estrategias/custom projects hay y cuales estan vigentes/obsoletos.
allowed-tools: Bash(python engine/*), Read, Write, Edit
---

# project-organizer — mantiene ordenado el proyecto STRATEGY QUANT

Esta skill encapsula la taxonomia de carpetas aprobada por el usuario en la reorganizacion de
2026-09-17 (ver [`user\PropFirm_Management\27_reorganizacion_estructural_proyecto.md`](../../../user/PropFirm_Management/27_reorganizacion_estructural_proyecto.md))
y da un flujo repetible para que la raiz **nunca vuelva a llenarse de archivos sueltos** a medida
que el usuario descargue mas material de biblioteca de StrategyQuant o cree nuevos proyectos.

No es un organizador generico de archivos: conoce el dominio (SQX, custom projects, MT5, ORB,
QlibSignal, etc.) mediante `taxonomy.json`, editable a mano cuando el proyecto evolucione.

**Prerequisito:** Python 3.8+ (solo standard library, sin instalar nada).

> Correr los comandos `python engine/...` desde la carpeta de esta skill (donde vive este
> `SKILL.md`), no desde el working directory del usuario.

## Las 5 categorias (fijas, ver `taxonomy.json` para el detalle completo)

| Carpeta | Que va aqui |
|---|---|
| `01_BIBLIOTECA_CONOCIMIENTO` | Skills, indicadores custom, plantillas `.cfx`, material de cursos/academia — se consulta, no se ejecuta como proyecto propio |
| `02_PROYECTOS_ACTIVOS` | Trabajo en desarrollo sobre un Custom Project/iniciativa con nombre propio (ORB, QlibSignal/ONNX, futuros) |
| `03_RESULTADOS` | Salidas generadas: reportes, CSV/JSON de export, XML de importacion, exports de databank |
| `04_HERRAMIENTAS_SCRIPTS` | Scripts `.py`/`.ps1`/`.bat` de proposito general, no atados a un solo proyecto |
| `05_ARCHIVO_DESCARTABLE` | Temporales/pruebas cerradas — se archivan, **nunca se borran automaticamente** |

`user\` **nunca se toca** (es espejo exacto de la instalacion real de SQX). Esta regla esta
codificada en `taxonomy.json:never_touch` y reforzada en `engine/apply_moves.py` (se niega a mover
cualquier cosa con ese nombre, sin excepcion, incluso si el usuario lo pide por error).

## Flujo de uso

### Caso A — "¿Quedó algo suelto en la raíz?" (auditoría periódica)

1. `python engine/scan_root.py` — lista todo lo que hay en la raiz que no esta ya en su lugar
   final (ni en `keep_in_root` ni dentro de una de las 5 carpetas).
2. Para cada resultado:
   - `OUT_OF_PROJECT` → no pertenece al proyecto en absoluto (ej. algo tipo Discord bot). Sugerir
     moverlo a `E:\VARIOS` (fuera del proyecto), confirmar con el usuario, luego usar el flujo de
     movimiento (paso 4).
   - `MATCHED_BUT_STILL_IN_ROOT` → ya sabemos a que categoria pertenece por su nombre; confirmar
     con el usuario en una linea y mover.
   - `UNCLASSIFIED` → ningun patron de nombre coincide. **No adivinar.** Ir al Caso B.
3. `python engine/validate.py` al final para confirmar que la raiz quedo limpia y `user\` intacto.

### Caso B — Material nuevo descargado (ej. nueva librería SQX) que no matchea ningún patrón

1. `python engine/classify.py "<ruta absoluta>"` — da `content_hint` (extensiones dominantes,
   si tiene `SKILL.md`/`README.md`, etc.) y devuelve `REQUIERE_CONFIRMACION_USUARIO` si no hay
   patron de nombre.
2. **Preguntar al usuario** (AskUserQuestion o texto) a qué categoría/subcarpeta pertenece,
   mostrando el `content_hint` como contexto. No decidir en su nombre.
3. Si el material nuevo define un patrón recurrente (ej. el usuario va a bajar 10 carpetas más con
   un prefijo similar), **actualizar `taxonomy.json`** agregando el `name_pattern` correspondiente
   a la categoría correcta, para que la próxima vez `scan_root.py` ya lo detecte solo.

### Caso C — Catálogo de contenido: qué ES cada cosa (no dónde vive)

Agregado 2026-09-16. Los Casos A/B de arriba solo deciden **en qué carpeta** vive un archivo
(biblioteca / proyecto activo / resultado / herramienta / descartable). Este caso responde una
pregunta distinta: de todo lo que ya está bien ubicado, **qué tipo de estrategia/artefacto es**
(breakout de sesión, mean-reversion, ML, filtro de cumplimiento...) y **si sigue vigente o quedó
obsoleto**. Cubre Custom Projects (`.cfx`), carpetas de portfolio bajo `user\projects\`, Custom
Blocks y Random Groups exportados como XML, e indicadores custom.

1. `python engine/scan_content.py` — escanea las ubicaciones declaradas en
   `taxonomy.json:content_catalog.scan_locations`, agrega los items nuevos a
   `content_catalog.json` con `status="pendiente_clasificar"` (nunca asigna tipo/estado solo) y
   marca `path_missing` en los que ya no existen en disco. Es de solo lectura sobre el proyecto.
2. Para cada item con `status="pendiente_clasificar"`: **preguntar al usuario** (no adivinar) a
   qué `strategy_type` y `status` pertenece — usar `python engine/classify_content.py "<ruta>"`
   sin flags para ver una pista de contenido superficial (símbolo/categoría/bloques detectados en
   el XML, conteo de `.sqx` en una carpeta de portfolio, etc.) como apoyo, nunca como decisión
   final.
3. Una vez confirmado con el usuario:
   `python engine/classify_content.py "<ruta>" --strategy-type <tipo> --status <estado> [--notes "..."]`
   — tipos y estados válidos están en `taxonomy.json:content_catalog.strategy_types`/`.status`
   (lista abierta, se puede agregar un `strategy_type` nuevo ahí si aparece un caso genuinamente
   distinto — no forzar algo en una categoría que no le calza).
4. `python engine/render_catalog.py` — regenera la vista humana en
   `01_BIBLIOTECA_CONOCIMIENTO\CATALOGO_PROYECTO.md` (agrupada por tipo de artefacto, con tabla
   de estado/tipo/notas). **No editar ese `.md` a mano** — se regenera desde
   `content_catalog.json`.
5. Re-correr `engine/scan_content.py` periódicamente (cada vez que se genere un nuevo Custom
   Project, bloque, o portfolio) para que el catálogo no se desactualice — mismo espíritu que el
   Caso A para la raíz.

### Ejecutar los movimientos

1. Construir un `mapping.json` (lista de `{"src": "...", "dest": "..."}`, rutas absolutas) con
   todos los movimientos ya confirmados por el usuario (Caso A + Caso B combinados).
2. `python engine/apply_moves.py mapping.json --dry-run` — valida sin mover nada; revisa que no
   haya `REFUSED_*`.
3. `python engine/apply_moves.py mapping.json` — ejecuta de verdad. Usa `git mv` si el repo tiene
   commits (preserva historial), si no, un move normal. Nunca sobreescribe un destino existente
   (falla explícito en vez de pisar datos) y nunca mueve nada del `never_touch`.
4. Revisar el log en `logs/moves_<timestamp>.jsonl`.
5. `python engine/validate.py` para confirmar el estado final.
6. **Registrar el cambio** en `user\PropFirm_Management\INDEX.md` (nueva fila) y su archivo de
   detalle, siguiendo el protocolo ya establecido del proyecto — esta skill no lo hace por sí sola,
   es un paso manual del agente al cerrar la tarea.

## Reglas no negociables

- Nunca se borra nada automáticamente. `05_ARCHIVO_DESCARTABLE` es un *staging area*, no una
  papelera — el usuario decide qué eliminar y cuándo.
- Nunca se toca `user\`.
- Nunca se sobreescribe un destino ya existente — un conflicto de nombres se reporta, no se
  resuelve en silencio.
- Ante un archivo/carpeta que no matchea ningún patrón conocido, **se pregunta al usuario**, no se
  adivina por contenido. `classify.py` da pistas, nunca decide solo.
- Igual principio aplica al catálogo de contenido: `scan_content.py` nunca asigna `strategy_type`/
  `status` por su cuenta — todo item nuevo entra como `pendiente_clasificar` hasta que el usuario
  lo confirme vía `classify_content.py`.
- El catálogo de contenido (Capa 2) solo cubre lo que resulta de **ejecutar** algo
  (`02_PROYECTOS_ACTIVOS`, `03_RESULTADOS`, `user\projects`) — material de
  `01_BIBLIOTECA_CONOCIMIENTO` (plantillas, skills descargadas, insumos externos) queda fuera,
  se deja tal como llegó (decisión del usuario, 2026-09-16, ver `content_catalog.json` →
  `_criterio_scope`).
- **Protocolo de cierre de sesión** (ver `CLAUDE.md` de la raíz del proyecto, sección 5): al
  cerrar sesión, el agente corre siempre `scan_content.py` → si hay items nuevos, pregunta al
  usuario tipo/estado y los clasifica con `classify_content.py` → regenera `render_catalog.py`.
  Si `scan_content.py` no encuentra nada nuevo, no hace falta preguntar nada más.
- `taxonomy.json` es la única fuente de verdad de las reglas — si el proyecto cambia de forma
  (nueva categoría, nuevo patrón, nuevo tipo de estrategia), se edita ahí, no se hardcodea en los
  scripts.

## Archivos de esta skill

- `taxonomy.json` — reglas de clasificación de carpetas (categorías, patrones de nombre,
  `never_touch`, `keep_in_root`, `out_of_project`) **y** el esquema del catálogo de contenido
  (`content_catalog`: kinds, strategy_types, status, scan_locations). Editar aquí cuando el
  proyecto evolucione.
- `engine/scan_root.py` — auditoría de solo lectura de la raíz.
- `engine/classify.py` — sugiere destino para una entrada puntual + pista de contenido.
- `engine/apply_moves.py` — ejecuta un mapping de movimientos ya confirmado, con salvaguardas.
- `engine/validate.py` — invariantes finales (raíz limpia, `user\` intacto, sin duplicados).
- `engine/scan_content.py` — detecta Custom Projects/portfolios/bloques/indicadores nuevos y los
  agrega a `content_catalog.json` como `pendiente_clasificar`.
- `engine/classify_content.py` — asigna `strategy_type`/`status`/notas a un item ya detectado
  (con confirmación del usuario) y muestra una pista de contenido superficial.
- `engine/render_catalog.py` — regenera `01_BIBLIOTECA_CONOCIMIENTO\CATALOGO_PROYECTO.md` (vista
  humana) a partir de `content_catalog.json`.
- `content_catalog.json` — fuente de verdad del catálogo de contenido (generado/editado por los
  tres scripts de arriba, no a mano salvo corrección puntual).
- `logs/` — historial de movimientos ejecutados (`.jsonl`, uno por corrida).
