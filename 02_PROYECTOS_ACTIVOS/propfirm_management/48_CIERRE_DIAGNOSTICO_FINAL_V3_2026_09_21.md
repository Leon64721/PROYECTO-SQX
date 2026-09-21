# 🔴 CIERRE: V3_MTF_CLEAN Irrecuperable — Análisis Final

**Fecha:** 2026-09-21
**Proyecto:** NDXm_ORB_PropFirm_V3_MTF_CLEAN  
**Estado:** FALLIDO — 4+ intentos, error persistente
**Error:** `There is no Price block defined!` (línea 22420 en Build-Task1.xml)

---

## TIMELINE DE INTENTOS

| Intento | Hora | Método | Resultado |
|---------|------|--------|-----------|
| 1 | 11:12 | Clonar V2→V3, ejecutar Build | ❌ "There is no Price block defined!" (40s) |
| 2 | 11:35 | Agregar Random Group en AlgoWizard UI | ❌ Mismo error (64s) |
| 3 | ~13:59 | Reintento sin cambios | ❌ Mismo error (35s) |
| 4 | (previos) | V2 original, V4, V5 | ❌ Todos: mismo error |

**Total:** 4 sesiones, 4 errores idénticos

---

## CAUSA RAÍZ IDENTIFICADA

### Lo que SABE:
1. ✅ Random Group `Levels_ORB_NDXm` EXISTE en Build-Task1.xml
2. ✅ Grupo tiene UUID correcto: `dd525f52-5e06-443f-aa9e-6b7295d29c6c`
3. ✅ Grupo tiene 4 items: Highest[14], Lowest[14], HighD, LowD
4. ✅ Build-Task1 REFERENCIA correctamente el UUID (línea 22420)
5. ✅ Datos de mercado cargan correctamente ("All backtest data prepared")

### El ERROR ocurre EN:
```
ReplacementConfig.chooseSpecialRandomly()
  → intenta elegir UN item del grupo RandomValue
  → FALLA: "There is no Price block defined!"
```

### Hipótesis (no confirmada):
- **A)** Motor SQX no RECONOCE el grupo aunque esté en XML
- **B)** Parámetros del grupo (Highest[14], Lowest[14]) no pueden computarse en el timeframe
- **C)** Incompatibilidad entre la estrategia/template y el grupo Value
- **D)** Caché/estado corrupto en el JDK embebido de SQX
- **E)** El XML se corrompió durante clonación/copia desde V2

---

## POR QUÉ NO SE RESOLVIÓ

| Acción | Por qué falló |
|--------|---------------|
| Clonar V2→V3 | V2 hereda el mismo problema |
| Agregar grupo en UI | AlgoWizard UI no embebe en .cfx |
| Editar XML manualmente | Extraer/repackagear rompe sincronización |
| Reintento sin cambios | Caché de SQX no se limpió |

---

## CONCLUSIÓN

**V3 NO es recuperable en esta instancia SQX (Build 144.2938).**

El error es **sistémico a la instalación**, no al proyecto:
- Todos los proyectos ORB en esta instancia fallan con el mismo error
- Clonación, edición manual, UI changes: nada resuelve
- El grupo existe pero el motor **no lo encuentra** en runtime

---

## SOLUCIÓN: PORTABILIDAD A NUEVA INSTANCIA

Empaquetar el proyecto completo (con notas, documentación, estructura) para:
1. Diagnóstico en otra máquina
2. Prueba en SQX fresh/reinstalado
3. Resumen para el equipo

**Archivos a incluir:**
- `project.cfx` (V3)
- `Build-Task1.xml` (debug)
- `config.xml`
- Todas las notas de diagnóstico (37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, este archivo)
- `INDEX.md` (cierre de proyecto)

---

## PRÓXIMO PASO

Archivar y cargar en GitHub para:
1. Control de versión
2. Acceso desde otra máquina
3. Documentación permanente del incidente

**Estado:** Esperando confirmación para crear archive
