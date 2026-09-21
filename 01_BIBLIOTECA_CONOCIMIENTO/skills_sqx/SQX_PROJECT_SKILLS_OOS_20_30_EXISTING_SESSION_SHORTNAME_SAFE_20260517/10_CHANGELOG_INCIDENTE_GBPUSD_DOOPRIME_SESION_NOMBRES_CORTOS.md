# CHANGELOG — Incidente GBPUSD DooPrime Cent: sesión y nombres cortos

## Contexto

El usuario solicitó 4 Custom Projects para GBPUSD DooPrime Cent. Las primeras versiones importaban con errores de recursos en SQX.

## Línea de aprendizaje

### V3

```text
Sesión usada: FX_XCCY_Currency1[DOOPRIME]
Resultado: error de recurso.
Causa: se mezcló el broker profile [DOOPRIME] con el Session Name.
```

### V4

```text
Sesión usada: FX_XCCY_Currency1DOOPRIME
Resultado: error al actualizar ZIP interno.
Causa: la sesión existía, pero fue incrustada/embebida como recurso nuevo dentro del .cfx.
```

### V5

```text
Sesión core/existente, sin sesión embebida, LimitTimeRange=false.
Resultado: abrió.
Aprendizaje: no forzar recurso de sesión nuevo.
```

### V6

```text
Sesión broker existente FX_XCCY_Currency1DOOPRIME referenciada, <Sessions /> vacío.
Resultado: E1/E2 abrieron; E3 falló.
Causa probable: Project name largo y carpeta/ruta interna problemática.
```

### V7

```text
Sesión existente referenciada.
<Sessions /> vacío.
LimitTimeRange=false.
Project names cortos: GBPDP_E1_H4PB_V7, GBPDP_E2_H4BO_V7, GBPDP_E3_H1MR_V7, GBPDP_E4_H1MO_V7.
Resultado: funcionaron los 4 customs.
```

## Reglas permanentes

```text
No inferir sesiones desde broker profile.
No incrustar sesiones existentes sin donor probado.
No activar LimitTimeRange=true sin donor probado.
No usar Project names largos.
No reutilizar nombres fallidos.
Importar desde C:\SQX_IMPORT\.
Borrar carpetas fallidas en user/projects antes de probar correcciones.
```

## Regla para otros brokers

Para cualquier broker nuevo:

```text
1. Pedir captura de Data Manager > Sessions.
2. Tomar el Session Name literal.
3. Si es sesión existente: referenciarla y dejar <Sessions /> vacío.
4. Si se necesita horario nativo: pedir donor .cfx probado.
5. Generar Project name corto.
```
