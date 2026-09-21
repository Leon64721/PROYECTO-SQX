# ORDEN DE TRABAJO SQX (Generada Automáticamente)

Inicia el flujo completo SQX Custom Project para **[NDXm_TICK_UTCPlus02]** en bróker **[Tickmill - Nasdaq]** capital **[500 usd]** con **5** edges y temporalidad candidata **[M3, M15, H1]**.

## Datos Operativos
- **Costos Inyectados:**
  - Spread: 1.0 pips
  - Slippage: 0 pips
  - Comisión: $0.0
  - Pip/Tick size: 0.01
  - Point value en $: 1
  - Swap Long/Short: -4.95 / -1.3
- **Rango de Data / Filtros:** 2015-01-01 / 2025-01-01

## Reglas Estrictas (Skills Activas: Forzar OOS 20-30%, Existing Session Safe, ShortName Safe (<=25), Custodia Limpia)
Usa la base custodia limpia como contenedor técnico. Reconstruye Builder, Edges, Ranking, Filtros y Robustez desde cero segun data, regimen, costes y objetivo. No heredes configuración de la base salvo justificación.
Ejecuta diagnostico de regimen, selección de ventanas IS/OOS (20-30%), configuración completa builder, OOS, MC_TRADES, MC_SPREAD slippage, TICK, SPP, WFM, auditoria anti-residuos, Databank chain, symbol Resource exact y operators safe.
**Entrega el .cfx importable con reporte minucioso y shortname safe.**

Notas Adicionales:

