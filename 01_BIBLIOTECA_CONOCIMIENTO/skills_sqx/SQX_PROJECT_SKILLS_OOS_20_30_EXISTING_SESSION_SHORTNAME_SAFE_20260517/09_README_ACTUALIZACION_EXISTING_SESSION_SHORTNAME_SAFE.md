# README — Actualización Existing Session + ShortName Safe

## Qué se corrigió

Se corrigieron dos causas reales de error en StrategyQuant X al importar Custom Projects:

```text
Cannot resolve custom resources
Failed to update zip content
```

Causas confirmadas:

1. Sesiones existentes en Data Manager incrustadas dentro del `.cfx` como si fueran recursos nuevos.
2. Project names largos que pueden romper la actualización del `project.cfx` interno o dejar carpetas corruptas en `user/projects`.

## Regla central de sesiones

Si la sesión ya existe en Data Manager:

```text
Usar el nombre exacto como referencia funcional.
No incrustar <Session> dentro del .cfx.
Dejar <Sessions /> vacío.
Mantener LimitTimeRange=false salvo donor probado.
No usar Add new al importar.
```

Para usar filtro horario nativo o incrustar una sesión:

```text
Se exige donor .cfx creado en SQX, exportado, reimportado y probado con Start.
```

## Regla central de nombres

```text
Project name preferido: <=25 caracteres.
Project name máximo: <=30 caracteres.
Nombre de archivo preferido: <=35 caracteres.
Ruta de importación: C:\SQX_IMPORT\.
```

Ejemplo correcto:

```text
GBPDP_E3_H1MR_V7
```

Ejemplo incorrecto:

```text
GBPUSD_DP_E3_H1_MEAN_REVERSION_BOTH_V6_BROKERSESSION_EXISTING
```

## Qué debe revisar el usuario al cargar nuevas fuentes

1. Retirar versiones anteriores de Skill 1, 2, 3 y 4.
2. Cargar este paquete completo.
3. Enviar captura de Data Manager > Sessions si quiere usar sesión de broker.
4. Si quiere horario nativo, enviar donor `.cfx` probado.
5. Importar los customs desde ruta corta.
6. Borrar carpetas fallidas en `user/projects` antes de reimportar correcciones.

## Resultado esperado

Cada nuevo Custom Project debe reportar explícitamente:

```text
Session mode.
Session name literal.
Si <Sessions /> va vacío o viene de donor.
LimitTimeRange.
Project name.
Longitud del Project name.
Estado ShortNameSafe.
Estado Session Existing Resource Safe.
```
