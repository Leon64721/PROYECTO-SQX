# FIX RÁPIDO: Agregar Price Block a V3_MTF_CLEAN — 5 minutos

**Problema:** V3 hereda XML incompleto de V2 → falta Random Group VALUE (Price block)

**Solución:** Agregar el grupo directamente en AlgoWizard UI

---

## PASOS (en SQX)

### 1. Cierra SQX completamente
```
tasklist | findstr StrategyQuant
```
Asegúrate que NO hay procesos corriendo.

---

### 2. Abre SQX y carga V3_MTF_CLEAN
- Ejecuta: `C:\SQX_144_Full\StrategyQuantX.exe`
- File → Open
- Navega a: `C:\SQX_144_Full\user\projects\NDXm_ORB_PropFirm_V3_MTF_CLEAN`
- Abre: `project.cfx`

---

### 3. Crea Random Group VALUE (Price Levels)
- En la izquierda, busca: **AlgoWizard → Random Groups**
- Click derecho → **New Group**
- Configura:
  ```
  Name: "Levels_ORB_NDXm"
  Type: VALUE (price levels)
  ```
- Agrega items (click "+ Add Item"):
  - `Highest[1]` — prior day high
  - `Lowest[1]` — prior day low
  - Número constante: `100` (para SL base)

---

### 4. Asigna el grupo al Build-Task1
- Selecciona: **Build-Task1** (BS-NDXm_ORB_MTF)
- Tab: **Building Blocks** o **Genetic Options**
- Busca dónde se asignan grupos aleatorios
- Selecciona: **Levels_ORB_NDXm** para el slot VALUE/price levels

---

### 5. Guarda el proyecto
- File → Save (o Ctrl+S)
- Verifica que no hay errores

---

## Luego: Build → OOS (FASE 1)

1. Build-Task1 → Run
2. Espera a que termine (30-40 min)
3. OOS corre automáticamente
4. **CHECKPOINT:** ¿Sobrevivientes > 0?

---

## Si aún falla con "There is no Price block defined"

Significa que el UI no permitió asignar el grupo. En ese caso, vuelvo a GENERACIÓN DESDE CERO con skills (menos probable ahora que agregamos el grupo manualmente).

---

**TIEMPO TOTAL:** 5 min (UI manual) + 1 hora (Build+OOS) = 1h 5 min

**GO cuando quieras →** Avisame cuando comiences en SQX

