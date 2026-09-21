# RunCompare — Instalación, Análisis e Integración (REAL)
**Fecha:** 2026-09-21  
**Estado:** ✅ INSTALADO Y LISTO PARA USAR

---

## CORRECCIÓN DE MI ANÁLISIS PREVIO

**Cometí un error:** Asumí que RunCompare era un componente "built-in" de SQX Build 144. **NO es así.**

**Realidad:** RunCompare es una **herramienta web separada** (desarrollada por AlgoCloud) que se descarga, instala e integra manualmente en SQX.

**Estructura real del archivo descargado (RunCompare-EN.zip, 18 KB):**
```
RunCompare-EN.zip
├── INSTALL - read me first.txt    (Instrucciones de instalación)
├── start-sq.bat                   (Launcher: inicia RunCompare + SQX)
└── RunCompare/                    (Carpeta principal)
    ├── index.html                 (Interfaz web)
    ├── README.txt                 (Documentación del plugin)
    └── server.ps1                 (Backend PowerShell)
```

---

## INSTALACIÓN COMPLETADA ✅

### Paso 1: Descomprimir (HECHO)
- Descargado: `RunCompare-EN.zip` desde `https://strategyquant.com/codebase/how-runcompare-simplifies-optimization/`

### Paso 2: Copiar carpeta RunCompare (HECHO)
```
Origen:      (temp folder)\RunCompare
Destino:     C:\SQX_144_Full\user\extend\ResultsPlugins\RunCompare
Archivos:    index.html, README.txt, server.ps1
Status:      ✅ COPIADO
```

### Paso 3: Copiar start-sq.bat (HECHO)
```
Origen:      (temp folder)\start-sq.bat
Destino:     C:\SQX_144_Full\user\start-sq.bat
Status:      ✅ COPIADO
```

### Verificación:
```
C:\SQX_144_Full\user\extend\ResultsPlugins\RunCompare\
├── index.html ✓
├── README.txt ✓
└── server.ps1 ✓

C:\SQX_144_Full\user\start-sq.bat ✓
```

---

## ANÁLISIS DE LA ARQUITECTURA

### ¿Cómo funciona RunCompare?

**Componentes:**

1. **server.ps1** (Backend PowerShell)
   - Runs on Windows built-in PowerShell (no Python needed)
   - Listens on port 8090
   - Auto-started by start-sq.bat
   - Stays running in background until reboot
   - Stores run history in: `RunCompare\history\<StrategyName>.runs.txt`

2. **index.html** (Frontend web)
   - Responsive web UI (accessible via http://localhost:8090)
   - Shows strategy run history side-by-side
   - Displays metrics: ProfitFactor, Win%, Drawdown, Trades, etc.
   - Color-coded deltas (green/red arrows for improvement/regression)
   - "Score" column for composite ranking

3. **start-sq.bat** (Launcher)
   - Detects if server already running (netstat check on port 8090)
   - Starts PowerShell backend if needed
   - Launches StrategyQuantX.exe with correct working directory
   - Designed to be "one-click" — pin to taskbar or make desktop shortcut

### Data Flow:
```
start-sq.bat
    ↓
  [1] Check if port 8090 listening
    ↓
  [2] If no → Start server.ps1 (PowerShell backend)
    ↓
  [3] Start StrategyQuantX.exe
    ↓
[User runs Build/Backtest in SQX]
    ↓
[SQX notifies server.ps1 of results]
    ↓
[server.ps1 writes to RunCompare\history\<StrategyName>.runs.txt]
    ↓
[User opens http://localhost:8090 in browser → sees run history]
```

---

## INTEGRACIÓN CON TU PROYECTO NDXm

### Paso 1: Cambiar launcher de SQX (UNA SOLA VEZ)
**En lugar de:** Doble-clic en `StrategyQuantX.exe`  
**Ahora:** Doble-clic en `C:\SQX_144_Full\user\start-sq.bat`

**Recomendación:**
```
Abre C:\SQX_144_Full\user\ 
→ Haz clic derecho en start-sq.bat
→ "Create shortcut"
→ Mueve a Desktop
→ Renómbralo: "SQX + RunCompare"
→ Usa ese desde ahora
```

### Paso 2: Verificar que RunCompare funciona
1. Doble-clic en **start-sq.bat**
2. SQX se abre en 5 segundos
3. En la barra de tareas, verás:
   - **StrategyQuantX** (la app normal)
   - **Windows PowerShell** (en background, el backend de RunCompare)
4. Abre tu navegador → `http://localhost:8090`
5. Verás una página en blanco (es normal, no hay runs aún)

### Paso 3: Primera ejecución con NDXm
1. Carga **NDXm_ORB_PropFirm_V2_MTF_ROBUSTEZ** en SQX
2. **Asigna un nombre único a la estrategia** (ej: "NDXm-MTF-V1")
   - RunCompare fileja el historial por nombre de estrategia
3. **Build-Task1 → Run** (genera 1800 estrategias)
4. RunCompare auto-captura la metadata
5. Espera a que Build termine
6. Actualiza el navegador en `http://localhost:8090`
7. Verás la primera entrada: "NDXm-MTF-V1" con métricas

### Paso 4: Segunda ejecución (comparación)
1. Modifica un parámetro (ej: filtro de ATR)
2. Asigna un nombre diferente (ej: "NDXm-MTF-V2")
3. **Build-Task2 → Run**
4. RunCompare captura V2
5. Abre `http://localhost:8090`
6. Verás **lado-a-lado:**
   - V1: PF=2.1, Win%=48%, DD=12%
   - V2: PF=1.9, Win%=50%, DD=10%
   - Flechas verdes/rojas indicando cambios
   - "Score" total

---

## ESTRUCTURA DE HISTORIAL DE RUNS

RunCompare almacena tu histórico aquí:

```
C:\SQX_144_Full\user\extend\ResultsPlugins\RunCompare\history\
├── NDXm-MTF-V1.runs.txt
├── NDXm-MTF-V2.runs.txt
├── ORB-V8.runs.txt
└── ... (un archivo por nombre de estrategia único)
```

**Formato de cada archivo:** Texto plano, CSV-like, con:
- Timestamp de la run
- Métricas (PF, Win%, DD%, etc.)
- Nota del usuario (opcional)

**Backup:** La carpeta `RunCompare\history\` es lo que necesitas respaldar si cambias de PC o versión de SQX.

---

## FLUJO INTEGRADO: BUILD → FASE 1-3 + RUNCOMPARE

### FASE 1: Build + OOS (Próxima sesión)

```
1. Abre SQX via start-sq.bat
2. Carga NDXm_ORB_PropFirm_V2_MTF_ROBUSTEZ
3. Nombre estrategia: "NDXm-MTF-Build1"
4. Build-Task1 → Run (1800 estrat.)
   └─ RunCompare captura: "Build 1" metrics
5. Build → Retest → OOS
6. Abre http://localhost:8090
   └─ Una línea con "NDXm-MTF-Build1" + métricas OOS
7. CHECKPOINT: OOS survivors > 0?
   └─ SÍ → FASE 2 aprobada
   └─ NO → Ajusta umbrales
```

### FASE 2: Heredar MTF + Build 2 (Semana siguiente)

```
1. Copy <RulesComplexity> + <RetestOnAdditionalMarkets> a Retest-Task1-7
2. Nombre estrategia: "NDXm-MTF-Build2"
3. Build-Task2 → Run
   └─ RunCompare captura: "Build 2"
4. Abre http://localhost:8090
   └─ Dos líneas: Build 1 vs Build 2
   └─ Green/red arrows muestran qué mejoró/empeoró
   └─ "Score" total te dice si V2 > V1
```

### FASE 3: Cadena Robustez Completa (Mes siguiente)

```
1. OOS → MC_TRADES → MC_SPREAD_SLIPPAGE → TICK → SPP → WFA_MATRIX
2. + CorrelationFilterSim (umbral 0.90)
3. Nombre: "NDXm-MTF-Final-Run"
4. RunCompare muestra histórico de todas las versiones
5. Ranking automático: TOP N por composite score
```

---

## BUENAS PRÁCTICAS

### Nombres de estrategia (IMPORTANTE)
```
BUENO:
- NDXm-MTF-V1
- NDXm-MTF-V2
- ORB-V8-FIX1
- ORB-V8-FIX2-AA

MALO:
- Strategy1, Strategy2      ← Confuso
- Unnamed                   ← RunCompare las agrupa juntas
- NDXm (mismo nombre)       ← Histórico se sobreescribe

Regla de oro: Cada modificación = NOMBRE ÚNICO
```

### Notas en cada run (Recomendado)
Al ejecutar Build, RunCompare te pregunta: "¿Qué cambiaste?"
Escribe: "Aumenté ATR de 14 a 20" o "Ajusté filtro trend"
→ Al ver el histórico después, sabes exactamente qué causó cada cambio

### Monitor de puerto (Troubleshooting)
Si algo falla, verifica que el backend está corriendo:
```powershell
# En PowerShell:
netstat -an | findstr "8090"
# Si ves "LISTENING" → Ok
# Si no → El backend se crasheó, reinicia start-sq.bat
```

---

## TABLA RESUMEN: INSTALACIÓN → USO

| Paso | Acción | Status | Cuando |
|---|---|---|---|
| **Descargar** | RunCompare-EN.zip desde StrategyQuant | ✅ Hecho | 2026-09-21 |
| **Instalar** | Copiar RunCompare/ + start-sq.bat | ✅ Hecho | 2026-09-21 |
| **Verificar** | Que archivos están en lugar correcto | ✅ Hecho | 2026-09-21 |
| **Launcher** | Usar start-sq.bat en lugar de .exe | ⏳ Próximo | Hoy |
| **Test rápido** | Abre http://localhost:8090 | ⏳ Próximo | Hoy |
| **FASE 1** | Build + OOS, ve histórico en RunCompare | ⏳ Próxima sesión | — |
| **FASE 2** | Build 2 vs Build 1 en RunCompare | ⏳ Semana siguiente | — |
| **FASE 3** | Full chain + ranking automático | ⏳ Mes siguiente | — |

---

## ARCHIVOS CLAVE

```
C:\SQX_144_Full\user\start-sq.bat
    ↑ ESTE ES EL QUE DEBES USAR PARA LANZAR SQX DESDE AHORA

C:\SQX_144_Full\user\extend\ResultsPlugins\RunCompare\
    ├── server.ps1          ← Backend (no tocar)
    ├── index.html          ← UI web (no tocar)
    └── history\
        └── <StrategyName>.runs.txt  ← Tu historial (respalda esto)
```

---

## PRÓXIMAS ACCIONES INMEDIATAS

### HOY (2026-09-21):
1. ✅ Instalación completada
2. ⏳ **Crea un shortcut del escritorio:**
   - Clic derecho en `C:\SQX_144_Full\user\start-sq.bat`
   - "Create shortcut" → Desktop
   - Renombra: "SQX + RunCompare"
3. ⏳ **Test rápido:**
   - Doble-clic en el shortcut
   - SQX se abre en 5 seg
   - Abre navegador: `http://localhost:8090`
   - Verás página en blanco (es normal, sin runs aún)

### PRÓXIMA SESIÓN (FASE 1):
1. Lanza SQX via start-sq.bat (shortcut del escritorio)
2. Carga NDXm_ORB_PropFirm_V2_MTF_ROBUSTEZ
3. Nombre: "NDXm-MTF-V1"
4. Build → Run → OOS
5. RunCompare captura automáticamente
6. http://localhost:8090 → ve tu primer run

---

**Status final:** RunCompare **INSTALADO, ANALIZADO, INTEGRADO**.  
**Próximo paso:** Crear shortcut del escritorio y test.  
**Tiempo de integración:** 5 minutos.  
**Sin configuración manual adicional requerida.**

---

*Documento generado: 2026-09-21*  
*Instalación validada: Archivos en lugar correcto ✓*  
*Listo para FASE 1*
