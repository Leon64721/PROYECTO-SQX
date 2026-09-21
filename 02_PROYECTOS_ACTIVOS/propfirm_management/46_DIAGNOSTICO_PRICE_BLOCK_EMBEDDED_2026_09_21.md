# 🔴 Diagnóstico: Price Block NO embebido en .cfx

**Problema:** V3_MTF_CLEAN hereda XML incompleto de V2 + Random Group agregado en UI NO se embebió

**Raíz:** El .cfx es un ZIP. Agregar grupos en AlgoWizard UI NO los inserta en el XML del .cfx.

---

## ¿Por qué falló agregar el grupo en UI?

```
Flujo esperado:
AlgoWizard UI → New Group → Save → Embebido en project.cfx

Flujo actual:
AlgoWizard UI → New Group → (Guardado solo en memoria/local, NO en .cfx)
Build-Task1 intenta acceder → "There is no Price block defined!"
```

**La UI permite crear grupos, pero el Build-Task1 solo ve lo que está EN EL XML del .cfx.**

---

## Solución: Generar .cfx Nuevo con sqx-strategy-project

**La skill `sqx-strategy-project` EMBEBE los grupos en el .cfx durante la generación.**

Voy a:
1. Generar Random Group (ya lo hicimos en `out/Levels_ORB_NDXm.xml`)
2. Generar Template MTF (con sqx-strategy-template)
3. Generar .cfx completo con el grupo EMBEBIDO (sqx-strategy-project)
4. Deploy en SQX
5. Build → OOS (debería funcionar)

---

## Timeline

- **Ahora:** Generar grupos + template + .cfx (~10 min)
- **Luego:** User cierra SQX, deploy new .cfx (~5 min)
- **Luego:** Build → OOS en nuevo proyecto (~1 hora)

---

## Go?

Si aceptas esperar 10 min más, genero el .cfx nuevo SIN el problema heredado de V2.

¿Continuamos?
