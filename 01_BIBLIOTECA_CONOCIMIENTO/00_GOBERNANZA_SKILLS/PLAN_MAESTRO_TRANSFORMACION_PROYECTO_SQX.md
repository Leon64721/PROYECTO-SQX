Contenido completo del archivo Markdown
Copiar
# PLAN MAESTRO DE TRANSFORMACIÓN DEL PROYECTO SQX

## Sistema integrado de skills, agentes, validación, coordinación y control de avances

---

## 0. IDENTIFICACIÓN DEL DOCUMENTO

| Campo | Valor |
|---|---|
| Proyecto | PROYECTO-SQX |
| Repositorio | `https://github.com/Leon64721/PROYECTO-SQX` |
| Instalación activa de StrategyQuant X | `C:\SQX_144_Full` |
| Documento | Plan maestro de transformación |
| Versión | 1.1 |
| Estado general | EN FASE 0 — PREPARACIÓN Y AUDITORÍA |
| Fecha de creación | 2026-09-21 |
| Responsable | Usuario del proyecto |
| Coordinador técnico | Asistente intermediario entre usuario, VS Code, Claude y StrategyQuant X |
| Fuente principal | Este documento y sus documentos complementarios |
| Ubicación recomendada | `01_BIBLIOTECA_CONOCIMIENTO/00_GOBERNANZA_SKILLS/` |

---

# 1. PROPÓSITO

Este documento define la arquitectura, el plan de trabajo y las reglas de coordinación para transformar `PROYECTO-SQX` en un sistema organizado de skills y agentes especializados.

El objetivo es que Claude, Claude Code, VS Code y las herramientas de StrategyQuant X puedan trabajar de forma:

- Separada.
- Reproducible.
- Controlada.
- Validable.
- Documentada.
- Modular.
- Escalable.
- Compatible con el conocimiento existente.
- Protegida contra la mezcla de contextos.

Este documento no es una simple guía informativa.

Es el **documento maestro de gobernanza del proyecto**.

Debe consultarse antes de:

- Crear estrategias.
- Crear Custom Projects.
- Crear o modificar bloques.
- Crear grupos.
- Crear plantillas.
- Trabajar con el agente de trading.
- Trabajar con Qlib.
- Trabajar con ONNX.
- Modificar código Java de SQX.
- Ejecutar validaciones de robustez.
- Analizar resultados.
- Aplicar reglas de prop firm.
- Desplegar archivos hacia `C:\SQX_144_Full`.

---

# 1-A. FASE INICIAL OBLIGATORIA: AUDITORÍA DE SKILLS Y FUENTES

Antes de crear, integrar o modificar cualquier skill, bloque, grupo, plantilla o Custom Project, se debe ejecutar una auditoría completa del repositorio en modo **solo lectura**.

Esta auditoría:

- Será **exclusivamente de lectura**, sin modificar archivos.
- **No creará nuevas skills**.
- **No creará bloques, grupos, plantillas ni Custom Projects**.
- **No generará estrategias**.
- **No modificará la instalación activa**.
- **No ejecutará deployments**.

El objetivo es conocer el **inventario real** antes de diseñar la integración definitiva.

## Flujo de auditoría

```text
Auditoría del repositorio
        ↓
Inventario de skills y herramientas
        ↓
Clasificación por frentes
        ↓
Identificación de dependencias
        ↓
Identificación de duplicados y conflictos
        ↓
Revisión humana del informe
        ↓
Creación del registro oficial
        ↓
Creación de la matriz de activación
        ↓
Integración controlada
```

## Objetivos de la auditoría inicial

- Identificar todas las skills existentes.
- Identificar herramientas y motores auxiliares.
- Identificar procedimientos operativos.
- Identificar validadores.
- Identificar scripts Python.
- Identificar código Java relacionado con SQX.
- Identificar archivos `.cfx`, `.sqx`, `.xml`, `.json` y `.csv`.
- Identificar fuentes de conocimiento.
- Identificar duplicados.
- Identificar solapamientos.
- Identificar conflictos entre skills.
- Identificar dependencias.
- Identificar archivos obsoletos.
- Identificar archivos experimentales.
- Identificar fuentes activas.
- Identificar qué componentes están pendientes de integración.
- Identificar qué skills pertenecen a cada frente.

## Alcance de la auditoría

La auditoría debe revisar como mínimo:

- `.claude/`
- `.claude/skills/`
- `01_BIBLIOTECA_CONOCIMIENTO/`
- `01_BIBLIOTECA_CONOCIMIENTO/skills_sqx/`
- `01_BIBLIOTECA_CONOCIMIENTO/academia_descargas/`
- `01_BIBLIOTECA_CONOCIMIENTO/custom_indicators/`
- `01_BIBLIOTECA_CONOCIMIENTO/VolumeProfile/`
- Scripts Python
- Código Java relacionado con SQX
- Archivos SKILL.md
- Archivos README.md
- Archivos CLAUDE.md
- Archivos .cfx
- Archivos .sqx
- Archivos .xml
- Archivos .json
- Archivos .csv
- Archivos de checksum
- Archivos de manifest
- Archivos de changelog
- Archivos de procedimientos

**Importante:** La auditoría debe analizar el **contenido real de los archivos**, no solamente sus nombres.

## Categorías oficiales de clasificación

Cada componente debe clasificarse con UNA O MÁS de estas categorías:

- `ROUTER` — Enrutador de solicitudes
- `ORCHESTRATOR` — Orquestador de tareas
- `CUSTOM_BLOCKS` — Bloques personalizados
- `GROUPS` — Grupos de bloques
- `TEMPLATES` — Plantillas de estrategia
- `CUSTOM_PROJECTS` — Proyectos .cfx
- `STRATEGY_GENERATION` — Generación de estrategias
- `TRADING_AGENT` — Agente de trading
- `QLIB_ONNX` — Puente Qlib→ONNX→SQX
- `PROPFIRM` — Reglas de prop firm
- `BROKER_DATA` — Datos y sesiones
- `ROBUSTNESS` — Validación de robustez
- `WFA` — Walk Forward Analysis
- `PORTFOLIO_ANALYSIS` — Análisis de portafolios
- `JAVA_SQX` — Código Java de SQX
- `PYTHON_AUTOMATION` — Automatización Python
- `DEPLOYMENT` — Despliegue
- `DOCUMENTATION` — Documentación
- `ARCHIVE` — Archivado
- `EXPERIMENTAL` — Experimental
- `UNKNOWN` — Desconocido

**Aclaración:** Un archivo puede tener múltiples categorías cuando corresponda, pero cada clasificación debe justificarse.

## Formato obligatorio del registro de cada skill

```
ID:
Nombre:
Ruta:
Categoría:
Frente:
Propósito:
Estado:
Documento principal:
Archivos complementarios:
Entradas:
Salidas:
Dependencias:
Validadores:
Scripts asociados:
Archivos que puede modificar:
Archivos protegidos:
Cuándo se activa:
Cuándo no se activa:
Skills relacionadas:
Conflictos:
Nivel de confianza:
Observaciones:
```

## Estados de auditoría

- `NO_AUDITADA` — No ha sido revisada
- `AUDITADA` — Revisada y clasificada
- `ACTIVA` — En uso activo
- `PENDIENTE_DE_INTEGRACION` — Audita pero sin integrar
- `INCOMPLETA` — Funcional pero no terminada
- `EXPERIMENTAL` — En fase de prueba
- `DUPLICADA` — Replica de otra existente
- `SOLAPADA` — Conflicta con otra
- `CONFLICTIVA` — Tiene conflictos no resueltos
- `OBSOLETA` — Ya no se usa
- `ARCHIVADA` — Guardada, no activa
- `DESCONOCIDA` — No se clasifica

**Importante:** `AUDITADA` no significa necesariamente `APROBADA` ni `INTEGRADA`.

## Entregables obligatorios de la fase de auditoría

La fase solo se cierra cuando se haya generado:

- `REGISTRO_DE_SKILLS.md` — Inventario completo
- `INFORME_AUDITORIA_SKILLS.md` — Análisis detallado
- `MATRIZ_DE_DEPENDENCIAS.md` — Relaciones entre skills
- `MATRIZ_DE_ACTIVACION.md` — Cuándo activar cada skill
- `INVENTARIO_DE_FUENTES.md` — Fuentes de verdad identificadas
- `LISTA_DE_CONFLICTOS_SKILLS.md` — Conflictos detectados

**Importante:** estos archivos son **entregables planificados**. No deben crearse todavía en esta tarea.

## Criterios de finalización de la auditoría

La fase solo podrá marcarse como completada cuando:

- [ ] Se haya revisado `.claude/`.
- [ ] Se haya revisado `01_BIBLIOTECA_CONOCIMIENTO/`.
- [ ] Se hayan revisado las skills de bloques.
- [ ] Se hayan revisado las skills de Custom Projects.
- [ ] Se haya revisado el material de sqx-lab.
- [ ] Se hayan revisado las skills de academia.
- [ ] Se hayan revisado scripts y herramientas.
- [ ] Se hayan identificado las fuentes de verdad.
- [ ] Se hayan identificado dependencias.
- [ ] Se hayan identificado duplicados.
- [ ] Se hayan identificado conflictos.
- [ ] Se haya generado el informe de auditoría.
- [ ] El informe haya sido revisado por el usuario.
- [ ] Se haya creado el registro oficial de skills.
- [ ] Se haya creado la matriz de activación.
- [ ] Se haya actualizado el plan maestro.

---

# 2. PROBLEMA QUE SE DEBE RESOLVER

Durante el desarrollo anterior se produjeron errores porque se mezclaban distintos frentes de trabajo.

Los principales problemas fueron:

1. Se utilizaban reglas de Custom Projects para tareas del agente de trading.
2. Se intentaba generar estrategias con el agente sin confirmar la integración Qlib → ONNX → SQX.
3. Claude recibía documentación, pero no siempre la consultaba.
4. Se generaban archivos nuevos cuando ya existían bases aprobadas.
5. Se utilizaban archivos antiguos como si fueran activos.
6. Se modificaban componentes que no pertenecían a la tarea.
7. Se mezclaba ORB clásico con Machine Learning sin solicitarlo explícitamente.
8. Se confundía el repositorio GitHub con la instalación activa de SQX.
9. Se declaraban tareas terminadas sin validarlas dentro de StrategyQuant.
10. Se creaban proyectos sin confirmar broker, símbolo, timeframe, sesión o zona horaria.
11. Se intentaba resolver todo en una sola conversación sin separar responsabilidades.
12. No existía un sistema único para marcar lo completado, pendiente o rechazado.
13. No existían contratos claros entre las diferentes skills.
14. No estaba definido cuándo una skill debía llamar a otra.
15. No había una matriz formal de activación y exclusión.

La solución será construir una arquitectura con:

```text
Router
    ↓
Orquestador
    ↓
Skill especializada
    ↓
Herramientas específicas
    ↓
Validación independiente
    ↓
Despliegue controlado
    ↓
Registro de resultados
3. PRINCIPIO FUNDAMENTAL
Ninguna tarea debe ejecutarse directamente a partir de una petición ambigua.

Antes de trabajar, se debe identificar:

Copiar
Frente:
Objetivo:
Tipo de tarea:
Skill principal:
Skills auxiliares:
Skills excluidas:
Archivos que deben consultarse:
Archivos que pueden modificarse:
Fuente de verdad:
Dependencias:
Validaciones:
Resultado esperado:
Información faltante:
Si faltan datos críticos, la tarea debe quedar en estado:

Copiar
[?] PENDIENTE DE INFORMACIÓN
Claude no debe inventar los datos faltantes.

4. ALCANCE DEL PROYECTO
Este plan organiza los siguientes ámbitos:

Custom Projects clásicos.
Generación de estrategias.
Agente de trading.
Qlib → ONNX → SQX.
Bloques personalizados.
Groups y Templates.
StrategyQuant Authoring Toolkit / sqx-lab.
Configuración de datos.
Broker, instrumentos y sesiones.
Gestión de prop firm.
Validación de robustez.
Walk Forward.
Análisis de resultados.
Análisis de portafolios.
Código Java personalizado de SQX.
Scripts Python.
Despliegue.
Sincronización entre GitHub y C:\SQX_144_Full.
Documentación.
Control de versiones.
Registro de incidentes.
Custodia de bases limpias.
5. SEPARACIÓN ENTRE REPOSITORIO E INSTALACIÓN ACTIVA
5.1 Repositorio del proyecto
El repositorio contiene principalmente:

Documentación.
Skills.
Scripts.
Configuraciones.
Bases de proyectos.
Código fuente.
Resultados seleccionados.
Historial de decisiones.
Conocimiento del proyecto.
Material de investigación.
El repositorio no representa automáticamente el estado actual de StrategyQuant X.

5.2 Instalación activa
La instalación activa está ubicada en:

Copiar
C:\SQX_144_Full
Rutas relevantes:

Copiar
C:\SQX_144_Full\internal\
C:\SQX_144_Full\j64\
C:\SQX_144_Full\user\data\
C:\SQX_144_Full\user\log\
C:\SQX_144_Full\user\projects\
C:\SQX_144_Full\user\extend\
C:\SQX_144_Full\user\extend\Snippets\
La instalación activa contiene:

Ejecutables.
Licencia.
JDK embebido.
Librerías internas.
Datos históricos.
Databanks.
Logs.
Proyectos utilizados por SQX.
Código desplegado.
Snippets.
Extensiones.
Configuraciones activas.
5.3 Regla de sincronización
Nunca se debe asumir que:

Copiar
Repositorio GitHub = Instalación activa de SQX
Antes de declarar que una modificación está activa, se debe confirmar:

Copiar
Archivo fuente:
Ubicación en el repositorio:
Archivo desplegado:
Ubicación desplegada:
Fecha de despliegue:
Versión:
Hash o checksum:
Prueba realizada:
Resultado:
5.4 Estados de sincronización
Cada componente puede estar en uno de estos estados:

Copiar
REPOSITORY_ONLY
ACTIVE_INSTALLATION_ONLY
SYNCHRONIZED
OUT_OF_SYNC
PENDING_DEPLOYMENT
DEPLOYED_NOT_VALIDATED
VALIDATED_AND_DEPLOYED
OBSOLETE
6. FRENTES OFICIALES DEL PROYECTO
Cada tarea debe pertenecer a uno y solo uno de estos frentes principales, salvo que se declare explícitamente una integración.

6.1 Frente CUSTOM_PROJECTS
Objetivo
Crear, modificar y validar Custom Projects .cfx de StrategyQuant X utilizando reglas clásicas o configuraciones definidas.

Ejemplos
ORB.
Breakouts.
Indicadores técnicos.
Filtros de volumen.
ATR.
SMA.
EMA.
Configuraciones multitemporales.
Salida al final del día.
Gestión monetaria.
Proyectos específicos por broker y activo.
No debe mezclarse automáticamente con
Copiar
TRADING_AGENT
QLIB_ONNX
6.2 Frente STRATEGY_GENERATION
Objetivo
Generar estrategias mediante StrategyQuant X bajo una configuración definida.

Incluye:

Builder.
Reglas de entrada.
Reglas de salida.
Filtros.
Money Management.
Restricciones.
OOS.
Robustez.
Selección de estrategias.
Puede trabajar con:

Reglas clásicas.
Señales ML.
Bloques personalizados.
Pero siempre debe indicar explícitamente cuál de esos modos está activo.

6.3 Frente TRADING_AGENT
Objetivo
Desarrollar el bot o agente de trading.

Incluye:

Arquitectura del agente.
Lógica de decisión.
Señales.
Entradas.
Salidas.
Gestión de estado.
Evaluación de señales.
Integración con StrategyQuant.
Flujo de generación basado en el agente.
No debe asumir automáticamente
Copiar
ORB
Custom Project clásico
Qlib
ONNX
Prop Firm
Cada integración debe solicitarse y documentarse.

6.4 Frente QLIB_ONNX
Objetivo
Construir y validar el puente:

Copiar
Qlib → Modelo → ONNX → QlibSignal → StrategyQuant X
Debe controlar
Datos de entrada.
Features.
Orden de características.
Normalización.
Tipos.
Dimensiones.
Horizonte.
Timeframe.
Valores nulos.
Preprocesamiento.
Inferencia.
Salida del modelo.
Compatibilidad con QlibSignal.
6.5 Frente CUSTOM_BLOCKS
Objetivo
Crear, revisar, documentar y validar bloques personalizados para StrategyQuant.

Ejemplos
Copiar
ORBLongBreakout
ORBShortBreakout
QlibSignal
Filtros de sesión
Filtros de volumen
Condiciones personalizadas
Indicadores personalizados
Reglas de salida
Un bloque no se considera listo solo porque se generó un XML.

Debe pasar por validación.

6.6 Frente GROUPS_TEMPLATES
Objetivo
Crear grupos y plantillas válidas a partir de bloques disponibles y validados.

Ejemplos de grupos
Copiar
GROUP_ORB_ENTRIES
GROUP_ORB_FILTERS
GROUP_ML_SIGNALS
GROUP_VOLUME_PROFILE
GROUP_SESSION_FILTERS
GROUP_PROP_FIRM_EXITS
Ejemplos de plantillas
Copiar
TEMPLATE_ORB_CLASSIC
TEMPLATE_ORB_MULTITIMEFRAME
TEMPLATE_ML_SIGNAL
TEMPLATE_VOLUME_PROFILE
6.7 Frente PROPFIRM
Objetivo
Aplicar y validar reglas de cuentas de prop firm.

Incluye:

Drawdown.
Daily Loss Limit.
Consistencia.
Noticias.
Rollover.
Zona horaria.
Comisiones.
Swaps.
Exposición.
Pérdidas diarias.
Cierre de sesión.
Reglas específicas de cada firma.
La lógica de prop firm debe operar como:

Copiar
Capa de restricciones
+
Capa de validación
No debe modificar automáticamente todos los Custom Projects.

6.8 Frente BROKER_DATA_SESSION
Objetivo
Definir las condiciones reales del activo y del broker.

Incluye:

Broker.
Símbolo.
Instrumento.
Contrato.
Timeframe.
Spread.
Comisión.
Swap.
Zona horaria.
Horario.
Sesiones.
Rollover.
Datos históricos.
Costos reales.
Especificaciones de ejecución.
6.9 Frente ROBUSTNESS
Objetivo
Validar la estabilidad de las estrategias.

Incluye:

OOS.
Monte Carlo de operaciones.
Monte Carlo de spread y slippage.
TICK.
SPP.
WFA Matrix.
Sensibilidad.
Degradación.
Estabilidad temporal.
Robustez de parámetros.
6.10 Frente RESULTS_PORTFOLIOS
Objetivo
Analizar los resultados generados.

Incluye:

Estrategias generadas.
Estrategias supervivientes.
Estrategias descartadas.
Portafolios.
Correlaciones.
Concentración.
Análisis mensual.
Aportes por activo.
Aportes por estrategia.
Estabilidad.
Degradación.
6.11 Frente SQX_JAVA_CUSTOM_CODE
Objetivo
Trabajar con código Java personalizado dentro de StrategyQuant.

Incluye:

Snippets.
Columnas de Databanks.
Lógica de prop firm.
Calendario de noticias.
Cálculos personalizados.
Integraciones internas.
Debe distinguirse entre:

Copiar
Código compilable de forma independiente
y:

Copiar
Código dependiente del entorno interno de StrategyQuant
6.12 Frente DEPLOYMENT_SYNC
Objetivo
Controlar el paso entre el repositorio y la instalación activa.

Incluye:

Backup.
Checksums.
Compilación.
Copia.
Verificación.
Logs.
Reversión.
Confirmación de que SQX está usando el archivo correcto.
7. ARQUITECTURA GENERAL DE AGENTES Y SKILLS
Copiar
                         ┌────────────────────────┐
                         │ PROJECT_ROUTER_SQX     │
                         │ Clasifica la solicitud │
                         └────────────┬───────────┘
                                      │
                         ┌────────────▼───────────┐
                         │ SQX_PROJECT_ORCHESTRATOR│
                         │ Coordina el flujo       │
                         └────────────┬───────────┘
                                      │
       ┌──────────────────────────────┼──────────────────────────────┐
       │                              │                              │
       ▼                              ▼                              ▼
CUSTOM_PROJECTS                 TRADING_AGENT                  ANALYSIS
       │                              │                              │
       ▼                              ▼                              ▼
CFX Skills                      QLIB_ONNX                    WFA / Portfolio
       │                              │                              │
       └───────────────┬──────────────┴──────────────┬───────────────┘
                       ▼                             ▼
              SQX AUTHORING TOOLKIT          PROPFIRM_COMPLIANCE
              Blocks / Groups / Templates     Riesgo / Noticias /
              Projects                        Rollover / Consistencia
                       │
                       ▼
              VALIDATION_PIPELINE
                       │
                       ▼
              DEPLOYMENT_VALIDATOR
                       │
                       ▼
              INSTALLATION ACTIVE SQX
8. INVENTARIO DE SKILLS
8.1 Router
Skill	Nombre	Estado
Router	PROJECT_ROUTER_SQX	[ ] Pendiente de formalizar
Orquestador	SQX_PROJECT_ORCHESTRATOR	[ ] Pendiente de formalizar
8.2 Authoring Toolkit
Skill	Función	Estado
Blocks	Crear y validar bloques	[ ] Pendiente de auditar completamente
Groups	Crear grupos	[ ] Pendiente de auditar completamente
Templates	Crear plantillas	[ ] Pendiente de auditar completamente
Projects	Crear proyectos	[ ] Pendiente de auditar completamente
Doctor	Diagnóstico de instalación	[ ] Pendiente de ejecutar y documentar
Setup	Configuración de instalación	[ ] Pendiente de ejecutar y documentar
8.3 Skills existentes de bloques personalizados
Ruta:

Copiar
01_BIBLIOTECA_CONOCIMIENTO/skills_sqx/SQX_CUSTOM_BLOCKS_SKILL/
Componente	Estado
SKILL.md	[ ] Pendiente de auditoría completa
README.md	[ ] Pendiente de auditoría completa
ORB_Breakout_Rules.xml	[ ] Pendiente de validación
engine/assess.py	[ ] Pendiente de auditoría
engine/bootstrap.py	[ ] Pendiente de auditoría
engine/check_specs.py	[ ] Pendiente de auditoría
engine/discover.py	[ ] Pendiente de auditoría
engine/emit.py	[ ] Pendiente de auditoría
engine/grammar.py	[ ] Pendiente de auditoría
engine/validate.py	[ ] Pendiente de auditoría
8.4 Skills existentes de Custom Projects
Ruta:

Copiar
01_BIBLIOTECA_CONOCIMIENTO/skills_sqx/SQX_PROJECT_SKILLS_OOS_20_30_EXISTING_SESSION_SHORTNAME_SAFE_20260517/
Skill	Responsabilidad	Estado
Skill 1	Generación de CFX	[ ] Pendiente de integración
Skill 2	Validación robusta	[ ] Pendiente de integración
Skill 3	Orquestador Custom Project	[ ] Pendiente de integración
Skill 4	Custodia de bases limpias	[ ] Pendiente de integración
8.5 Skills de análisis
Skill	Función	Estado
WFA	Análisis Walk Forward	[ ] Pendiente de integrar
Portafolio	Análisis mensual	[ ] Pendiente de integrar
Resultados	Análisis de estrategias	[ ] Pendiente de integrar
Prop Firm	Validación de reglas	[ ] Pendiente de integrar
Broker	Datos y sesiones	[ ] Pendiente de integrar
Despliegue	Sincronización	[ ] Pendiente de crear o integrar
9. RESPONSABILIDAD DE CADA COMPONENTE
9.1 PROJECT_ROUTER_SQX
Puede
Clasificar solicitudes.
Seleccionar skills.
Detectar ambigüedades.
Pedir información.
Bloquear una ejecución incorrecta.
No puede
Crear bloques.
Crear proyectos.
Modificar código.
Alterar configuraciones.
9.2 SQX_PROJECT_ORCHESTRATOR
Puede
Coordinar skills.
Ordenar etapas.
Revisar dependencias.
Enviar salidas de una skill a otra.
Generar informes.
No puede
Saltarse validaciones.
Cambiar el alcance sin autorización.
Sustituir el conocimiento especializado.
9.3 SQX_CUSTOM_BLOCKS
Puede
Crear bloques.
Validar bloques.
Documentar parámetros.
Analizar dependencias.
Emitir XML compatible.
No puede
Crear automáticamente un Custom Project final.
Activar Qlib sin solicitarlo.
Modificar prop firm.
Modificar proyectos base sin autorización.
9.4 CFX_GENERATOR
Puede
Crear una copia de trabajo.
Modificar configuraciones.
Crear .cfx.
Utilizar bases aprobadas.
No puede
Alterar directamente la base limpia.
Inventar nodos.
Inventar rutas.
Cambiar el alcance.
Crear bloques no validados.
9.5 CFX_ROBUSTNESS_VALIDATOR
Puede
Revisar OOS.
Revisar Monte Carlo.
Revisar TICK.
Revisar SPP.
Revisar WFA.
Rechazar proyectos.
No puede
Cambiar silenciosamente el proyecto.
Modificar la estrategia sin registrar el cambio.
Declarar robustez sin criterios definidos.
9.6 TRADING_AGENT
Puede
Diseñar el agente.
Definir señales.
Proponer reglas.
Trabajar con el flujo ML.
No puede
Crear Custom Projects clásicos automáticamente.
Activar ORB sin autorización.
Modificar la lógica de prop firm.
Cambiar el modelo ONNX sin aprobación.
9.7 QLIB_ONNX_BRIDGE
Puede
Revisar features.
Revisar modelos.
Validar ONNX.
Revisar inferencia.
Integrar QlibSignal.
No puede
Inventar columnas.
Cambiar el modelo sin registrar versión.
Crear un Custom Project completo automáticamente.
9.8 PROPFIRM_COMPLIANCE
Puede
Validar resultados.
Detectar incumplimientos.
Aplicar reglas configuradas.
Generar alertas.
No puede
Cambiar silenciosamente la estrategia.
Asumir rollover.
Asumir zona horaria.
Asumir que Order.PL equivale siempre al balance real.
10. INTEGRACIÓN DEL TOOLKIT SQX-LAB
El toolkit sqx-lab debe utilizarse como motor especializado para la autoría de StrategyQuant.

Flujo:

Copiar
Bloques
    ↓
Random Groups
    ↓
Strategy Templates
    ↓
Build Projects
10.1 Función de sqx-lab
Puede ayudar con:

Blocks.
Groups.
Templates.
Projects.
Catálogos.
Validación de referencias.
Compatibilidad con la instalación real.
Generación de artefactos de StrategyQuant.
10.2 No sustituye
sqx-lab no sustituye:

El router del proyecto.
La separación de frentes.
El agente de trading.
Qlib.
ONNX.
Prop Firm Compliance.
La validación económica.
La sincronización GitHub/SQX.
La toma de decisiones de trading.
El análisis final de resultados.
10.3 Acciones de integración
 Confirmar instalación del toolkit.
 Ejecutar /sqx-setup.
 Apuntar a la instalación activa.
 Ejecutar /sqx-doctor.
 Guardar diagnóstico.
 Revisar catálogo generado.
 Identificar rutas de salida.
 Identificar archivos modificables.
 Identificar validadores.
 Crear matriz de integración.
 Ejecutar prueba de bloque ORB.
 Ejecutar prueba de grupo.
 Ejecutar prueba de plantilla.
 Ejecutar prueba de proyecto.
11. FLUJO DE AUTORÍA DE STRATEGYQUANT
Etapa 1: bloque
Entrada:

Copiar
Especificación del bloque.
Salida:

Copiar
Bloque creado y validado.
Estado requerido:

Copiar
VALIDATED
Etapa 2: grupo
Entrada:

Copiar
Bloques validados.
Salida:

Copiar
Grupo creado y validado.
Estado requerido:

Copiar
VALIDATED
Etapa 3: plantilla
Entrada:

Copiar
Grupos validados.
Salida:

Copiar
Plantilla creada y validada.
Estado requerido:

Copiar
VALIDATED
Etapa 4: Custom Project
Entrada:

Copiar
Plantilla validada.
Grupos validados.
Bloques validados.
Datos confirmados.
Salida:

Copiar
Custom Project creado.
Estado requerido:

Copiar
VALIDATED
Regla de bloqueo
No se puede avanzar a una etapa si la anterior no está validada.

Copiar
Bloque no validado
    → No se crea grupo final

Grupo no validado
    → No se crea plantilla final

Plantilla no validada
    → No se crea Custom Project final

Custom Project no validado
    → No se ejecuta pipeline definitivo
12. MATRIZ DE ACTIVACIÓN
12.1 Crear un Custom Project ORB
Activar
Copiar
PROJECT_ROUTER_SQX
SQX_PROJECT_ORCHESTRATOR
SQX_CUSTOM_BLOCKS
SQX_GROUPS_AND_TEMPLATES
SQX_CUSTOM_PROJECT_AUTHORING
CFX_GENERATOR
CFX_ROBUSTNESS_VALIDATOR
CLEAN_BASE_CUSTODIAN
BROKER_DATA_SESSION
Activar opcionalmente
Copiar
PROPFIRM_COMPLIANCE
Desactivar
Copiar
TRADING_AGENT
QLIB_ONNX_BRIDGE
12.2 Generar estrategias con agente ML
Activar
Copiar
PROJECT_ROUTER_SQX
TRADING_AGENT
QLIB_ONNX_BRIDGE
SQX_CUSTOM_BLOCKS
SQX_GROUPS_AND_TEMPLATES
SQX_CUSTOM_PROJECT_AUTHORING
Activar posteriormente
Copiar
CFX_ROBUSTNESS_VALIDATOR
PROPFIRM_COMPLIANCE
SQX_RESULTS_ANALYZER
No activar automáticamente
Copiar
CFX_GENERATOR clásico ORB
12.3 Crear un bloque ORB
Activar
Copiar
PROJECT_ROUTER_SQX
SQX_CUSTOM_BLOCKS
No activar automáticamente
Copiar
GROUPS_TEMPLATES
CFX_GENERATOR
TRADING_AGENT
QLIB_ONNX_BRIDGE
12.4 Crear un bloque QlibSignal
Activar
Copiar
PROJECT_ROUTER_SQX
QLIB_ONNX_BRIDGE
SQX_CUSTOM_BLOCKS
Validar
Copiar
Modelo.
Entradas.
Salidas.
Tipos.
Dimensiones.
Normalización.
Timeframe.
Dependencias.
Compatibilidad con SQX.
12.5 Analizar WFA
Activar
Copiar
PROJECT_ROUTER_SQX
WFA_ANALYZER
SQX_RESULTS_ANALYZER
Desactivar
Copiar
SQX_CUSTOM_BLOCKS
CFX_GENERATOR
TRADING_AGENT
12.6 Validar prop firm
Activar
Copiar
PROJECT_ROUTER_SQX
PROPFIRM_COMPLIANCE
BROKER_DATA_SESSION
SQX_RESULTS_ANALYZER
No modificar automáticamente
Copiar
Bloques.
Plantillas.
Custom Projects.
Modelo ONNX.
13. DATOS OBLIGATORIOS POR TIPO DE TAREA
13.1 Para Custom Project
Copiar
Nombre del proyecto:
Activo:
Símbolo exacto:
Broker:
Timeframe principal:
Timeframe secundario:
Zona horaria:
Sesión:
Datos históricos:
Señales:
Filtros:
Entradas:
Salidas:
Money Management:
OOS:
Monte Carlo:
TICK:
SPP:
WFA:
Reglas de prop firm:
Ruta de salida:
13.2 Para agente de trading
Copiar
Objetivo del agente:
Activo:
Timeframe:
Fuente de datos:
Tipo de señal:
Modelo:
Versión del modelo:
Entrada:
Salida:
Horizonte:
Regla de decisión:
Regla de entrada:
Regla de salida:
Gestión de riesgo:
Plataforma objetivo:
Integración con SQX:
Validación:
13.3 Para Qlib → ONNX
Copiar
Modelo:
Versión:
Features:
Orden de features:
Dimensiones:
Tipos:
Normalización:
Horizonte:
Timeframe:
Entrada ONNX:
Salida ONNX:
Valores nulos:
Ejemplo de inferencia:
Bloque SQX:
13.4 Para bloques
Copiar
Nombre:
Tipo:
Propósito:
Entradas:
Salidas:
Parámetros:
Valores permitidos:
Dependencias:
Reglas:
Ejemplos:
Plataforma:
13.5 Para prop firm
Copiar
Firma:
Cuenta:
Zona horaria:
Hora de rollover:
Regla de Daily Loss:
Regla de drawdown:
Regla de consistencia:
Reglas de noticias:
Comisión:
Swap:
Spread:
Fuente oficial:
Método de cálculo:
14. CONTRATOS ENTRE SKILLS
14.1 Contrato de bloque
Entrada
Copiar
Nombre:
Propósito:
Tipo:
Entradas:
Salidas:
Parámetros:
Reglas:
Dependencias:
Plataforma:
Ejemplos:
Salida
Copiar
Archivo generado:
Especificación:
Versión:
Hash:
Dependencias:
Validación:
Estado:
Ubicación:
Estados:

Copiar
DRAFT
VALIDATED
REJECTED
DEPLOYED
DEPRECATED
14.2 Contrato de grupo
Entrada
Copiar
Nombre:
Propósito:
Bloques permitidos:
Bloques obligatorios:
Bloques excluidos:
Reglas de combinación:
Salida
Copiar
Grupo generado:
Bloques incluidos:
Bloques rechazados:
Validación:
Dependencias:
Estado:
Ubicación:
14.3 Contrato de plantilla
Entrada
Copiar
Nombre:
Tipo de estrategia:
Grupos:
Entradas:
Salidas:
Filtros:
Money Management:
Temporalidades:
Reglas obligatorias:
Reglas opcionales:
Salida
Copiar
Plantilla:
Dependencias:
Compatibilidad:
Validación:
Estado:
Ubicación:
14.4 Contrato de Custom Project
Entrada
Copiar
Nombre:
Activo:
Símbolo:
Broker:
Timeframe principal:
Timeframe secundario:
Zona horaria:
Sesión:
Datos:
Bloques:
Grupos:
Plantilla:
Builder:
Money Management:
OOS:
Monte Carlo:
TICK:
SPP:
WFA:
Prop Firm:
Salida
Copiar
Archivo CFX:
Versión:
Fuente base:
Cambios:
Hash:
Validaciones:
Pendientes:
Ubicación:
Estado:
14.5 Contrato de despliegue
Entrada
Copiar
Archivo fuente:
Versión:
Hash:
Destino:
Backup:
Motivo:
Pruebas requeridas:
Salida
Copiar
Archivo desplegado:
Ruta:
Fecha:
Hash:
Backup:
Resultado:
Logs:
Reversión disponible:
Estado:
15. FLUJO OBLIGATORIO DE CADA TAREA
Fase 1: clasificación
 Leer la solicitud.
 Identificar el frente.
 Confirmar el objetivo.
 Confirmar el tipo de tarea.
 Detectar ambigüedades.
Fase 2: selección de skills
 Seleccionar skill principal.
 Seleccionar skills auxiliares.
 Excluir skills no relacionadas.
 Definir dependencias.
Fase 3: alcance
 Definir archivos consultables.
 Definir archivos modificables.
 Definir archivos prohibidos.
 Definir si se trabaja en repositorio o instalación activa.
Fase 4: fuentes
 Consultar este documento.
 Consultar la skill principal.
 Consultar documentación especializada.
 Consultar la base aprobada.
 Confirmar versión.
 Confirmar estado de los archivos.
Fase 5: planificación
 Crear plan técnico.
 Definir etapas.
 Definir pruebas.
 Definir criterios de aprobación.
 Definir plan de reversión.
Fase 6: ejecución
 Trabajar solo dentro del alcance.
 No modificar archivos no autorizados.
 No mezclar frentes.
 Registrar cambios.
 Mantener copia de seguridad.
Fase 7: validación
 Validar estructura.
 Validar sintaxis.
 Validar dependencias.
 Validar referencias.
 Validar en StrategyQuant.
 Revisar logs.
 Validar resultado lógico.
 Validar resultado estadístico.
Fase 8: cierre
 Actualizar estado.
 Registrar archivos.
 Registrar pruebas.
 Registrar errores.
 Registrar pendientes.
 Actualizar changelog.
 Preparar commit si corresponde.
16. PROTOCOLO OBLIGATORIO PARA CLAUDE
Antes de ejecutar cualquier cambio, Claude debe producir:

Copiar
## Clasificación de la tarea

Frente:
Objetivo:
Tipo de tarea:
Skill principal:
Skills auxiliares:
Skills excluidas:
Archivos que se consultarán:
Archivos que pueden modificarse:
Archivos que no deben modificarse:
Fuente de verdad:
Dependencias:
Validaciones:
Resultado esperado:
Datos faltantes:
Si existen datos faltantes críticos, debe detenerse y preguntarlos.

Después de planificar
Claude debe mostrar:

Copiar
## Plan de ejecución

Fase 1:
Fase 2:
Fase 3:

Archivos que serán creados:
Archivos que serán modificados:
Archivos que permanecerán intactos:
Pruebas:
Criterios de aprobación:
Plan de reversión:
No debe modificar archivos antes de mostrar el plan cuando la tarea sea de alto impacto.

17. FORMATO DE CIERRE DE CADA TAREA
Copiar
## Informe de cierre

### Solicitud
Descripción breve.

### Frente
Frente utilizado.

### Estado
PENDIENTE / EN PROGRESO / VALIDADO / DESPLEGADO / RECHAZADO.

### Skills activadas
Lista completa.

### Skills excluidas
Lista completa.

### Archivos consultados
Lista completa.

### Archivos creados
Lista completa.

### Archivos modificados
Lista completa.

### Archivos protegidos
Archivos que no fueron modificados.

### Fuente de verdad
Archivo, instalación o catálogo utilizado.

### Cambios realizados
Descripción técnica.

### Validaciones ejecutadas
Lista de pruebas.

### Resultado
Descripción del resultado.

### Errores
Errores encontrados.

### Pendientes
Tareas pendientes.

### Despliegue
Indicar si se copió a `C:\SQX_144_Full`.

### Reversión
Indicar si existe backup y cómo revertir.

### Próximo paso
Siguiente acción recomendada.
18. REGLAS DE FUENTES DE VERDAD
18.1 Prioridad general
Copiar
1. Código probado en la instalación activa.
2. Resultado reproducible.
3. Configuración utilizada realmente por SQX.
4. Base limpia validada.
5. Bloque, grupo o plantilla validada.
6. Skill vigente.
7. Documentación oficial.
8. Documentación del proyecto.
9. Notas históricas.
10. Archivos experimentales.
11. Archivos archivados.
18.2 Estados documentales
Todo documento importante debe identificarse como:

Copiar
[ACTIVO]
[VALIDADO]
[EXPERIMENTAL]
[PENDIENTE_DE_CONFIRMAR]
[OBSOLETO]
[ARCHIVADO]
[RECHAZADO]
19. REGLAS SOBRE BASES LIMPIAS
Las bases limpias no deben modificarse directamente.

Flujo obligatorio:

Copiar
Base limpia
    ↓
Copia de trabajo
    ↓
Modificación
    ↓
Validación
    ↓
Comparación
    ↓
Nueva versión aprobada
Antes de crear una nueva versión se debe registrar:

Copiar
Base utilizada:
Versión:
Cambios:
Motivo:
Archivos afectados:
Resultado de validación:
Checksum:
Estado:
20. REGLAS DE BLOQUEO
La tarea debe detenerse si:

No se conoce el frente.
No se conoce el objetivo.
No se conoce el archivo fuente.
No se conoce el activo.
No se conoce el timeframe.
No se conoce el broker cuando sea relevante.
No se conoce la zona horaria.
No se conoce la sesión.
Se intenta utilizar una base no validada.
Se intenta modificar la instalación sin backup.
Se intenta mezclar ORB y ML sin solicitud explícita.
Se referencia un bloque inexistente.
Se referencia una plantilla no validada.
El diagnóstico de sqx-lab presenta errores críticos.
El proyecto no puede ser cargado por SQX.
La validación no es reproducible.
21. PROBLEMAS CONOCIDOS
21.1 Rollover
La agrupación por medianoche UTC no necesariamente representa el día operativo real de una cuenta prop firm.

Debe definirse:

Copiar
Zona horaria:
Hora de rollover:
Regla de horario de verano:
Día operativo:
21.2 Consistencia
No se debe asumir automáticamente que:

Copiar
Order.PL = impacto real sobre el balance
Debe revisarse:

Comisión.
Swap.
Ajustes.
Balance.
Delta de balance.
Método de cálculo de cada métrica.
21.3 Calendario de noticias
Debe validarse:

Archivo ausente.
CSV vacío.
Filas incompletas.
Fechas inválidas.
Horas inválidas.
Eventos duplicados.
Zonas horarias.
Ventanas de restricción.
21.4 Código dependiente de SQX
Algunos archivos Java pueden depender de:

SettingsMap.
Librerías internas.
Clases del motor.
APIs de StrategyQuant.
Entorno del Code Editor.
Una compilación externa no siempre demuestra compatibilidad completa con SQX.

21.5 Desincronización
El repositorio puede contener una versión distinta de:

Copiar
C:\SQX_144_Full
Debe verificarse siempre.

22. FASES DEL PLAN DE TRANSFORMACIÓN

Fase 0: Preparación y auditoría de skills
Objetivo:

Ejecutar auditoría completa del repositorio en modo solo lectura.
Identificar todas las skills existentes.
Clasificar por frentes.
Identificar dependencias y conflictos.
Crear registro oficial.

Entregables:

- REGISTRO_DE_SKILLS.md
- INFORME_AUDITORIA_SKILLS.md
- MATRIZ_DE_DEPENDENCIAS.md
- MATRIZ_DE_ACTIVACION.md
- INVENTARIO_DE_FUENTES.md
- LISTA_DE_CONFLICTOS_SKILLS.md

Estado:

 [ ] Auditoría de skills ejecutada.
 [ ] Informe de auditoría generado.
 [ ] Registro oficial creado.
 [ ] Matriz de activación creada.

Fase 1: Registro oficial de skills
Objetivo:

Formalizar el registro de auditoría.

Estado:

 [ ] Pendiente.

Fase 2: Mapa de frentes
Objetivo:

Separar formalmente las líneas de trabajo.

Entregable:

Copiar
MAPA_DE_FRENTES.md
Estado:

 Pendiente.
Fase 3: matriz de activación
Objetivo:

Definir qué skills se activan según cada solicitud.

Entregable:

Copiar
MATRIZ_DE_ACTIVACION.md
Estado:

 Pendiente.
Fase 4: contratos entre skills
Objetivo:

Definir entradas, salidas, estados y validaciones.

Entregable:

Copiar
SKILL_CONTRACTS.md
Estado:

 Pendiente.
Fase 5: integración de sqx-lab
Objetivo:

Analizar y conectar el toolkit oficial.

Tareas:

 Confirmar instalación.
 Ejecutar /sqx-setup.
 Ejecutar /sqx-doctor.
 Documentar rutas.
 Documentar catálogo.
 Documentar validadores.
 Documentar salidas.
 Crear matriz de integración.
Estado:

 Pendiente.
Fase 6: integración de bloques
Objetivo:

Probar creación y validación de un bloque.

Primera prueba:

Copiar
ORBLongBreakout
ORBShortBreakout
Estado:

 Pendiente.
Fase 7: integración de grupos
Objetivo:

Crear grupos utilizando únicamente bloques validados.

Estado:

 Pendiente.
Fase 8: integración de plantillas
Objetivo:

Crear plantillas utilizando únicamente grupos y bloques válidos.

Estado:

 Pendiente.
Fase 9: integración de Custom Projects
Objetivo:

Utilizar las cuatro skills existentes sin duplicarlas ni ignorarlas.

Estado:

 Pendiente.
Fase 10: integración de robustez
Objetivo:

Conectar:

Copiar
OOS
Monte Carlo
TICK
SPP
WFA
Estado:

 Pendiente.
Fase 11: integración de resultados
Objetivo:

Conectar resultados con:

Copiar
WFA
Portafolios
Prop Firm
Análisis mensual
Estado:

 Pendiente.
Fase 12: integración del agente ML
Objetivo:

Separar y conectar:

Copiar
Agente
Qlib
ONNX
QlibSignal
StrategyQuant
Estado:

 Pendiente.
Fase 13: despliegue controlado
Objetivo:

Validar el proceso hacia:

Copiar
C:\SQX_144_Full
Estado:

 Pendiente.
23. PRUEBAS DE ACEPTACIÓN
Prueba 1: bloque ORB
Objetivo:

Validar o crear un bloque ORB.

Condiciones:

 Se activa únicamente la skill de bloques.
 No se activa el agente ML.
 Se consulta la documentación correcta.
 Se valida el XML.
 Se documenta el resultado.
Estado:

 Pendiente.
Prueba 2: grupo ORB
Objetivo:

Crear un grupo con bloques validados.

Condiciones:

 Todos los bloques existen.
 Todos los bloques están validados.
 No hay referencias inválidas.
 El grupo es documentado.
Estado:

 Pendiente.
Prueba 3: plantilla ORB
Objetivo:

Crear una plantilla ORB.

Condiciones:

 Usa grupos válidos.
 Define entradas.
 Define salidas.
 Define filtros.
 Define money management.
 Pasa validación.
Estado:

 Pendiente.
Prueba 4: Custom Project ORB
Objetivo:

Crear un proyecto .cfx.

Condiciones:

 Se utiliza una base aprobada.
 Se confirma el activo.
 Se confirma broker.
 Se confirman timeframes.
 Se confirma zona horaria.
 Se confirma sesión.
 Se configura Builder.
 Se valida en SQX.
Estado:

 Pendiente.
Prueba 5: robustez
Objetivo:

Ejecutar el pipeline de robustez.

Condiciones:

 OOS.
 Monte Carlo.
 Spread/slippage.
 TICK.
 SPP.
 WFA.
 Informe de resultados.
Estado:

 Pendiente.
Prueba 6: análisis
Objetivo:

Analizar los resultados.

Condiciones:

 Se identifican estrategias supervivientes.
 Se separan descartadas.
 Se analiza estabilidad.
 Se analizan portafolios.
 Se registra la conclusión.
Estado:

 Pendiente.
Prueba 7: agente ML
Debe realizarse solamente después de validar las pruebas anteriores.

Condiciones:

 El modelo está identificado.
 ONNX está validado.
 Las features están documentadas.
 QlibSignal existe.
 El bloque es validado.
 El flujo de inferencia funciona.
 No se mezcla accidentalmente con ORB clásico.
Estado:

 Pendiente.
24. ESTRUCTURA DE CARPETAS RECOMENDADA
Copiar
01_BIBLIOTECA_CONOCIMIENTO/
└── 00_GOBERNANZA_SKILLS/
    ├── PLAN_MAESTRO_TRANSFORMACION_PROYECTO_SQX.md
    ├── MAPA_DE_FRENTES.md
    ├── REGISTRO_DE_SKILLS.md
    ├── MATRIZ_DE_ACTIVACION.md
    ├── SKILL_CONTRACTS.md
    ├── FUENTES_DE_VERDAD.md
    ├── PROTOCOLO_DE_VALIDACION.md
    ├── CHECKLIST_BLOCKS.md
    ├── CHECKLIST_GROUPS.md
    ├── CHECKLIST_TEMPLATES.md
    ├── CHECKLIST_CUSTOM_PROJECTS.md
    ├── CHECKLIST_ROBUSTEZ.md
    ├── CHECKLIST_PROPFIRM.md
    ├── CHECKLIST_DEPLOYMENT.md
    ├── HISTORIAL_DE_DECISIONES.md
    ├── INCIDENTES.md
    └── CHANGELOG_TRANSFORMACION.md
Las skills operativas de Claude deben estar en:

Copiar
.claude/skills/
La documentación de gobernanza debe estar en:

Copiar
01_BIBLIOTECA_CONOCIMIENTO/00_GOBERNANZA_SKILLS/
25. REGISTRO DE TAREAS
Cada tarea importante debe añadirse a una tabla como esta:

ID	Fecha	Frente	Tarea	Skill principal	Estado	Responsable	Resultado
T-001	2026-09-21	Gobernanza	Crear plan maestro	Orquestador	[~]	Usuario/Claude	En organización
T-002		Custom Blocks	Validar bloque ORB	Custom Blocks	[ ]		Pendiente
T-003		Custom Projects	Validar base CFX	CFX Custodian	[ ]		Pendiente
T-004		SQX-Lab	Ejecutar diagnóstico	SQX-Lab	[ ]		Pendiente
T-005		ML	Auditar QlibSignal	Qlib ONNX	[ ]		Pendiente
26. HISTORIAL DE DECISIONES
Cada decisión arquitectónica debe registrarse así:

Copiar
## DECISIÓN-001

Fecha:
Tema:
Problema:
Opciones consideradas:
Decisión:
Motivo:
Archivos afectados:
Impacto:
Estado:
Decisiones iniciales:

DECISIÓN-001 — Separar frentes
Fecha: 2026-09-21
Decisión: separar Custom Projects, agente ML, Qlib/ONNX, prop firm y análisis.
Motivo: evitar mezcla de contextos.
Estado: [V] Adoptada.
DECISIÓN-002 — Usar sqx-lab como motor de autoría
Fecha: 2026-09-21
Decisión: integrar sqx-lab, no reemplazarlo.
Motivo: ya contiene conocimiento y herramientas especializadas.
Estado: [V] Adoptada.
DECISIÓN-003 — Usar una capa de orquestación superior
Fecha: 2026-09-21
Decisión: crear router y orquestador.
Motivo: coordinar skills existentes.
Estado: [V] Adoptada.
DECISIÓN-004 — No modificar bases limpias directamente
Fecha: 2026-09-21
Decisión: utilizar copias de trabajo.
Motivo: proteger fuentes aprobadas.
Estado: [V] Adoptada.
27. FORMATO DE INCIDENTES
Copiar
## INCIDENTE-XXX

Fecha:
Frente:
Descripción:
Comportamiento esperado:
Comportamiento observado:
Archivo o skill implicada:
Causa:
Impacto:
Corrección:
Validación:
Prevención:
Estado:
Todo error repetitivo debe registrarse como incidente.

28. ACTUALIZACIÓN DEL PLAN
Este documento debe actualizarse cuando:

Se crea una skill.
Se modifica una skill.
Se integra una herramienta.
Se valida un bloque.
Se aprueba un grupo.
Se aprueba una plantilla.
Se crea un Custom Project.
Se completa una prueba.
Se descubre un error.
Se cambia una fuente de verdad.
Se modifica una ruta.
Se despliega una versión.
Se revierte un cambio.
Se cambia la arquitectura.
Se completa una fase.
Cada actualización debe registrar:

Copiar
Fecha:
Responsable:
Cambio:
Motivo:
Archivos afectados:
Pruebas:
Resultado:
Estado:
29. REGLA DE ACTUALIZACIÓN DE CHECKBOXES
Utilizar estos estados:

Copiar
- [ ] Pendiente
- [~] En progreso
- [?] Pendiente de información
- [V] Validado
- [D] Desplegado
- [R] Rechazado
- [A] Archivado
- [X] Cancelado
No marcar como [V] VALIDADO algo que solamente fue creado.

No marcar como [D] DESPLEGADO algo que solamente fue guardado en el repositorio.

No marcar como completada una tarea si sus pruebas están pendientes.

30. CRITERIOS PARA CONSIDERAR UNA TAREA COMPLETA
Una tarea solo está completa cuando:

 El frente está identificado.
 La skill correcta fue utilizada.
 Las skills incorrectas permanecieron desactivadas.
 Las fuentes fueron consultadas.
 El alcance fue respetado.
 Los archivos fueron documentados.
 El resultado fue generado.
 El resultado fue validado.
 Las pruebas fueron ejecutadas.
 Los errores fueron registrados.
 Los pendientes fueron identificados.
 El plan fue actualizado.
 El despliegue fue documentado si correspondía.
31. PROMPT DE INICIO PARA CLAUDE
Utilizar el siguiente prompt al iniciar una sesión de trabajo:

Copiar
Antes de realizar cualquier cambio en este proyecto, lee obligatoriamente:

01_BIBLIOTECA_CONOCIMIENTO/00_GOBERNANZA_SKILLS/PLAN_MAESTRO_TRANSFORMACION_PROYECTO_SQX.md

Este archivo es el plan maestro de coordinación del proyecto.

No ejecutes todavía ninguna modificación.

Primero debes:

1. Confirmar que encontraste y leíste el plan maestro.
2. Identificar todos los frentes de trabajo definidos.
3. Identificar las skills disponibles en el repositorio.
4. Identificar cuáles están activas, pendientes de auditar o sin integrar.
5. Revisar el estado general del plan.
6. Indicar qué skills deben permanecer desactivadas para la tarea actual.
7. Proponer únicamente el siguiente paso aprobado por el plan.
8. No crear bloques, grupos, plantillas, Custom Projects, código ni estrategias todavía.
9. No modificar ningún archivo.
10. No asumir que el repositorio y C:\SQX_144_Full están sincronizados.

Tu respuesta debe utilizar exactamente esta estructura:

## Confirmación de lectura

## Frentes detectados

## Skills encontradas

## Skills pendientes de auditoría o integración

## Diferencia entre repositorio e instalación activa

## Estado actual del plan

## Riesgos detectados

## Próximo paso recomendado

## Información faltante

## Archivos que no modificaré todavía
32. PROMPT DE CLASIFICACIÓN DE UNA TAREA
Copiar
Clasifica la siguiente solicitud dentro de la arquitectura del proyecto.

Solicitud:
[PEGAR SOLICITUD DEL USUARIO]

No ejecutes cambios todavía.

Debes identificar:

1. Frente principal.
2. Tipo de tarea.
3. Skill principal.
4. Skills auxiliares.
5. Skills que deben permanecer desactivadas.
6. Archivos que deben consultarse.
7. Archivos que podrían modificarse.
8. Datos faltantes.
9. Validaciones requeridas.
10. Resultado esperado.
11. Riesgos de mezclar esta tarea con otro frente.

Responde utilizando el formato definido en PLAN_MAESTRO_TRANSFORMACION_PROYECTO_SQX.md.
33. PROMPT DE PLANIFICACIÓN
Copiar
Utilizando el PLAN_MAESTRO_TRANSFORMACION_PROYECTO_SQX.md y las skills correspondientes, crea únicamente un plan técnico para la tarea siguiente:

[TAREA]

No modifiques archivos todavía.

El plan debe incluir:

1. Frente.
2. Objetivo.
3. Skill principal.
4. Skills auxiliares.
5. Skills excluidas.
6. Fuentes de verdad.
7. Archivos que deben consultarse.
8. Archivos que pueden modificarse.
9. Archivos protegidos.
10. Dependencias.
11. Etapas de ejecución.
12. Validaciones.
13. Criterios de aprobación.
14. Plan de reversión.
15. Informe final esperado.
16. Información que falta confirmar.

Detente al final del plan y espera aprobación.
34. PROMPT DE EJECUCIÓN CONTROLADA
Copiar
Ejecuta únicamente el plan aprobado para la tarea indicada.

No amplíes el alcance.

Antes de modificar archivos:

1. Confirma el frente.
2. Confirma las skills activas.
3. Confirma las skills excluidas.
4. Confirma los archivos permitidos.
5. Confirma la fuente base.
6. Crea backup si corresponde.
7. Registra la versión inicial.

Durante la ejecución:

- No modifiques archivos protegidos.
- No mezcles frentes.
- No inventes parámetros.
- No inventes rutas.
- No utilices archivos archivados como fuentes activas.
- No declares éxito antes de validar.

Al finalizar, entrega el informe de cierre definido en el plan maestro.
35. PROMPT DE VALIDACIÓN
Copiar
Valida el resultado de la tarea sin realizar cambios correctivos automáticamente.

Tarea:
[DESCRIPCIÓN]

Resultado:
[ARCHIVO, PROYECTO, BLOQUE, GRUPO, PLANTILLA O CÓDIGO]

Debes comprobar:

1. Estructura.
2. Sintaxis.
3. Referencias.
4. Dependencias.
5. Compatibilidad con la instalación activa.
6. Compatibilidad con StrategyQuant.
7. Cumplimiento del plan.
8. Cumplimiento de la skill utilizada.
9. Ausencia de mezcla con otros frentes.
10. Pruebas ejecutadas.
11. Errores.
12. Riesgos.
13. Recomendación: aprobar, rechazar o devolver para corrección.

No modifiques nada hasta presentar el informe de validación.
36. PRÓXIMO PASO OFICIAL
El próximo paso aprobado por este plan es:

Copiar
Auditar e inventariar todas las skills existentes.
El resultado debe ser:

Copiar
01_BIBLIOTECA_CONOCIMIENTO/00_GOBERNANZA_SKILLS/REGISTRO_DE_SKILLS.md
Después se debe crear:

Copiar
MATRIZ_DE_ACTIVACION.md
Después:

Copiar
SKILL_CONTRACTS.md
No se debe iniciar todavía una generación compleja de estrategias con el agente ML.

La primera prueba operativa será:

Copiar
Validar o crear un bloque ORB sin activar el frente del agente de trading.
37. HISTORIAL DE CAMBIOS

Versión 1.1 — 2026-09-21

- Se incorporó una fase obligatoria de auditoría antes del desarrollo.
- Se estableció que la auditoría será exclusivamente de lectura.
- Se definieron las categorías oficiales de clasificación.
- Se definieron los estados de auditoría.
- Se definieron los campos del registro de cada skill.
- Se definieron los entregables de la auditoría.
- Se establecieron los criterios de finalización.
- Se reorganizó el orden de las fases del proyecto.
- La Fase 0 es ahora la auditoría inicial obligatoria.
- No se modificaron skills existentes.
- No se modificó StrategyQuant X.
- No se modificó `C:\SQX_144_Full`.
- No se crearon bloques, grupos, plantillas ni Custom Projects.

Versión 1.0 — 2026-09-21

- Creado el plan maestro completo.
- Definidos los frentes oficiales.
- Definida la diferencia entre repositorio e instalación activa.
- Definida la arquitectura de router y orquestador.
- Incorporado sqx-lab.
- Incorporadas las skills de bloques personalizados.
- Incorporadas las cuatro skills de Custom Projects.
- Definida la cadena Blocks → Groups → Templates → Projects.
- Definida la matriz de activación.
- Definidos los contratos entre skills.
- Definido el protocolo de trabajo con Claude.
- Definidos los estados de avance.
- Definidos los criterios de tarea completa.
- Definidas las pruebas de aceptación.
- Definido el sistema de incidentes.
- Definido el sistema de decisiones.
- Definido el sistema de actualización del documento.
- Pendiente auditoría completa de los contenidos individuales.
- Pendiente guardar el documento en el repositorio.
- Pendiente actualizar CLAUDE.md.
38. ESTADO ACTUAL CONSOLIDADO

### Gobernanza

- [V] Arquitectura general definida.
- [V] Frentes principales definidos.
- [V] Problemas históricos identificados.
- [V] Reglas de separación definidas.
- [V] Flujo general definido.
- [V] Estados de avance definidos.
- [V] Formatos de trabajo definidos.
- [V] Plan maestro guardado en el repositorio.
- [V] Nombre del documento normalizado.

### Fase 0 — Auditoría inicial

- [ ] Auditoría de skills ejecutada.
- [ ] Informe de auditoría generado.
- [ ] Informe de auditoría revisado.
- [ ] Skills clasificadas.
- [ ] Dependencias identificadas.
- [ ] Duplicados identificados.
- [ ] Conflictos identificados.
- [ ] Fuentes de verdad identificadas.
- [ ] Registro oficial de skills creado.
- [ ] Matriz de activación creada.
- [ ] Contratos entre skills creados.

### Integración de StrategyQuant

- [ ] Toolkit `sqx-lab` auditado.
- [ ] `/sqx-setup` ejecutado.
- [ ] `/sqx-doctor` ejecutado.
- [ ] Catálogo de SQX revisado.
- [ ] Skill de Custom Blocks auditada.
- [ ] Skills de Custom Projects auditadas.

### Primera prueba operativa

- [ ] Bloque ORB seleccionado.
- [ ] Bloque ORB creado o validado.
- [ ] Bloque ORB probado.
- [ ] Grupo ORB creado.
- [ ] Plantilla ORB creada.
- [ ] Custom Project ORB de prueba creado.
- [ ] Custom Project ORB validado.
39. REGLA FINAL DEL PROYECTO
El sistema completo debe funcionar de esta manera:

Copiar
Solicitud del usuario
        ↓
Clasificación del frente
        ↓
Selección de skills
        ↓
Exclusión de skills incorrectas
        ↓
Consulta de fuentes de verdad
        ↓
Plan técnico
        ↓
Aprobación
        ↓
Ejecución controlada
        ↓
Validación independiente
        ↓
Despliegue si corresponde
        ↓
Registro del resultado
        ↓
Actualización del plan
Ninguna skill debe trabajar aislada cuando dependa de otra.

Ningún resultado debe considerarse definitivo sin validación.

Ningún frente debe activarse por inferencia cuando la solicitud sea ambigua.

Ninguna base limpia debe modificarse directamente.

Ningún archivo del repositorio debe considerarse instalado en SQX sin confirmación.

El proyecto debe avanzar por etapas pequeñas, verificables y documentadas.

Copiar

## Cómo guardarlo

1. Abre el repositorio en VS Code.
2. Crea la carpeta:

```text
01_BIBLIOTECA_CONOCIMIENTO/00_GOBERNANZA_SKILLS/
Crea el archivo:
Copiar
PLAN_MAESTRO_TRANSFORMACION_PROYECTO_SQX.md
Copia dentro todo el contenido anterior.
Guarda el archivo.
No lo coloques en la raíz.
Después crea un commit:
Copiar
git add 01_BIBLIOTECA_CONOCIMIENTO/00_GOBERNANZA_SKILLS/PLAN_MAESTRO_TRANSFORMACION_PROYECTO_SQX.md
git commit -m "docs: crear plan maestro de transformación y gobernanza de skills SQX"
git push
Importante
Este documento ya contiene el plan completo, pero el avance real todavía debe marcarse conforme se ejecuten las tareas. Por ejemplo, no debemos marcar como completado:

Copiar
- [V] Integración de sqx-lab
hasta que realmente se haya:

Ejecutado su configuración.
Ejecutado su diagnóstico.
Revisado su catálogo.
Probado su flujo.
Documentado su integración.
Validado contra la instalación activa de StrategyQuant.