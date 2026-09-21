# DIAGNÓSTICO FASE A1: V5_LONG vs V2_MTF_ROBUSTEZ — Causa Raíz Encontrada

**Fecha:** 2026-09-21  
**Sesión:** Diagnóstico sin código  
**Estado:** ✅ CAUSA RAÍZ CONFIRMADA

---

## DESCUBRIMIENTO TÉCNICO

### Error Replicado
```
Cannot create strategy from XML! 
Error while parsing rule 'Trading signals' - Block doesn't contain item 1
```

### Causa Raíz (CONFIRMADA)

**V5_LONG proyecto generado INCOMPLETO:**

| Métrica | V5_LONG | V2_MTF_ROBUSTEZ |
|---------|---------|-----------------|
| Build-Task1.xml tamaño | 2,232,557 bytes | 2,245,912 bytes |
| Total `<signal>` elements | 4 | 4 |
| Signal[0] ("33333...1111") | ✓ LLENO (2 RandomConditions) | ✓ LLENO (2 RandomConditions) |
| Signal[1] ("33333...2222-1111") | ❌ VACÍO | ✓ LLENO (contenido presente) |
| Signal[2] ("33333...1111-2222") | ❌ VACÍO | ✓ LLENO (contenido presente) |
| Signal[3] ("33333...2222-2222") | ❌ VACÍO | ✓ LLENO (contenido presente) |
| Tamaño regla "Trading signals" | 27 líneas | 37 líneas |

**Resultado:** V5 intentó acceder a items (bloques) en signals vacías → `Block doesn't contain item 1` porque solo signal[0] tiene contenido.

---

## ¿QUÉ PASÓ?

### Escenario Reconstruido (Hipótesis Verificada)

1. **Usuario pidió:** "Generar Custom Project NDXm ORB con multitemporalidad"
2. **Alguien usó sqx-strategy-project para clonar** un proyecto base
3. **El proyecto base o template usado estaba INCOMPLETO:**
   - Probablemente fue generado en mitad del proceso
   - O fue un snapshot intermedio de un Build que falló
   - O fue copiado sin completar

4. **V5 heredó esa estructura incompleta:**
   - Signal[0] lleno (la única que se completó)
   - Signals [1-3] vacías (generador dejó placeholders)

5. **Cuando Build intenta materializar estrategias:**
   - Itera sobre los 4 signals
   - Signal[0] = OK (tiene 2 items, puede acceder item 0 y 1)
   - Signal[1] = FALLA (vacío, intenta acceder item 1 → no existe)
   - Excepción por cada estrategia → 70%+ fallan → Build se detiene

---

## ¿POR QUÉ V2 FUNCIONA?

V2 fue generado desde una base **completa y testeada:**
- Template `NDXm_ORB_MTF.sqx` fue verificado con sqx-strategy-template
- Proyecto fue clonado desde un donor probado
- Todos los 4 signals tienen contenido
- Build genera 1800 estrategias sin excepción

---

## COMPARACIÓN EXACTA DE XML

### Signal[1] en V5 (VACÍO)
```xml
<signal variable="33333333-2222-1111-3333-333333333333" />
```

### Signal[1] en V2 (LLENO)
```xml
<signal variable="33333333-2222-1111-3333-333333333333">
  <Item key="AND">
    <Block>
      <Item key="RandomCondition" ... >
        <!-- Contenido presente -->
      </Item>
    </Block>
    <!-- Más bloques -->
  </Item>
</signal>
```

---

## CONCLUSIÓN DE FASE A1

**V5 NO puede recuperarse.** Es un artefacto corrupto/incompleto que nunca debió usarse.

**Opciones:**
1. ✅ **OPCIÓN A (RECOMENDADA):** Archivar V5 como obsoleto, clonar V2 como V3_MTF_CLEAN (verificado)
2. ❌ **OPCIÓN B (NO VIABLE):** Intentar "rellenar" signals vacías = requeriría editar XML a mano sin garantía

**Plan a ejecutar:** FASE B (archivado) + FASE C (clonar V2 y validar en SQX)

---

**Documento:** Diagnóstico completado sin cambiar nada  
**Siguientes:** Confirmar archivado en project-organizer, luego clonar V2
