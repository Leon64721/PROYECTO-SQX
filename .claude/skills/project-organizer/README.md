# project-organizer

Skill interna (no distribuible, especifica de este proyecto) para mantener ordenada la raiz de
`E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT` a medida que se agrega material nuevo (librerias SQX,
scripts, resultados de corridas, etc.).

Ver [`SKILL.md`](SKILL.md) para el flujo de uso completo. Resumen rapido:

```bash
cd .claude/skills/project-organizer

# 1. Auditar la raiz
python engine/scan_root.py

# 2. Clasificar una entrada puntual que no matcheo ningun patron
python engine/classify.py "E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\algo_nuevo"

# 3. Ejecutar movimientos ya confirmados (mapping.json: lista de {"src":.., "dest":..})
python engine/apply_moves.py mapping.json --dry-run
python engine/apply_moves.py mapping.json

# 4. Validar el estado final
python engine/validate.py
```

### Catálogo de contenido (qué ES cada Custom Project/estrategia/bloque)

```bash
# 1. Detectar items nuevos (Custom Projects .cfx, portfolios, bloques, indicadores)
python engine/scan_content.py

# 2. Ver pista de contenido de un item pendiente (no decide nada)
python engine/classify_content.py "E:\...\algo.cfx"

# 3. Asignar tipo/estado una vez confirmado con el usuario
python engine/classify_content.py "E:\...\algo.cfx" --strategy-type breakout_session --status vigente

# 4. Regenerar la vista humana
python engine/render_catalog.py
# -> 01_BIBLIOTECA_CONOCIMIENTO\CATALOGO_PROYECTO.md
```

Reglas duras: nunca toca `user\`, nunca borra nada, nunca sobreescribe un destino existente, nunca
adivina la categoria de algo desconocido (pregunta al usuario). Todo editable en `taxonomy.json`.
