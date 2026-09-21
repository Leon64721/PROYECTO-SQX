# Protocolo de Análisis Experto de Databanks (StrategyQuant X)

Este protocolo define cómo evaluar y filtrar estrategias generadas por StrategyQuant X usando nuestros scripts de Python personalizados, con especial énfasis en los resultados del Walk-Forward Analysis (WFA) y la eliminación de estrategias correlacionadas ("gemelas").

## 1. Exportación de Datos
1. El usuario debe exportar los resultados del databank deseado (preferiblemente el de WFA Matrix final) desde la interfaz de SQX (Seleccionar todas -> Click derecho en Databank -> Export to CSV).
2. Guardar el archivo en la estructura de proyecto local (ej. `E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT\Resultados Databank\`).

## 2. Herramientas Disponibles
En la raíz de este proyecto se encuentran dos scripts principales de análisis:
- **`analyze_wfa_databank.py`**: Optimizado para analizar la matriz final de WFA (CSV separados por `;`).
- **`analyze_databank.py`**: Uso general para otras exportaciones de resultados iniciales o genéricos.

## 3. Lógica del "Composite Score"
Los scripts ordenan las estrategias usando un sistema de puntuación compuesto (0 a 1) mediante normalización Min-Max:
- **60% Return/DD Ratio**: Priorizamos la estabilidad del capital, bajo Drawdown y retorno relativo (La métrica suprema).
- **40% Profit Factor**: Medida clásica de eficiencia en el trading (Groß/Loss).
- *Filtros duros (Base)*: Se descartan automáticamente estrategias con `< 50 trades` o `Profit Factor < 1.1`.

## 4. Análisis de No-Correlación (Prevención de Gemelos)
SQX a menudo genera variantes de la misma estrategia con ligeros cambios de parámetros (pero misma lógica estructural). Para garantizar que un portafolio de "Top 5" esté diversificado lógicamente:
1. El script lee el CSV y obtiene el nombre de la estrategia ganadora (ej. `Strategy 2.8.300`).
2. Navega al directorio de instalación/proyectos original de SQX (`C:\SQX_144_Full\user\projects\...\databanks`).
3. Abre internamente el `.sqx` (que funciona como un archivo ZIP) sin necesidad de API gráfica, y extrae el archivo `strategy_Portfolio.xml`.
4. Mediante expresiones regulares (Regex) lee la firma exacta de indicadores usados en la estrategia.
5. Si una estrategia candidata posee exactamente los mismos indicadores que una que ya ingresó al Top 5, **se descarta automáticamente**, garantizando un ranking libre de correlación estructural.

## 5. Ejecución Básica (CLI)
Cuando el usuario solicite analizar un nuevo databank:
```bash
python "analyze_wfa_databank.py"
```
*(Nota técnica: Dentro de los scripts, las rutas apuntan por defecto a `E:\...\DatabankExportWFAMATRIX.csv` y al directorio raíz del proyecto SQX en disco C:. Para nuevos proyectos, ajustar las variables `csv_path` y `sqx_dir` al inicio de `main()`).*
