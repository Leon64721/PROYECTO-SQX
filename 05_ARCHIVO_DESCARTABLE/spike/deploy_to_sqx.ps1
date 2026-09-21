<#
.SYNOPSIS
    Despliega los artefactos validados del puente Qlib->ONNX->SQX (Fase 3,
    Tarea T5 de user\Qlib_ONNX_Bridge_Design.md) desde el sandbox del
    proyecto (E:\...\STRATEGY QUANT) hacia la instalacion de produccion real
    de SQX (C:\SQX_144_Full).

.DESCRIPTION
    NO se ejecuto automaticamente -- este script se generó como entregable
    para revision y ejecución manual del usuario. C:\SQX_144_Full es la
    instalacion VIVA de SQX, actualmente en uso; escribir ahi sin que el
    usuario lo confirme/presencie no es una accion que Claude Code deba
    tomar unilateralmente (ver freeze boundary activo en este proyecto,
    puesto explicitamente por el usuario para proteger este directorio).

    Copia:
      1. spike\lib\onnxruntime-1.29.0.jar -> C:\SQX_144_Full\user\libs\
      2. qlib_export\output\model.onnx + feature_spec.json ->
         C:\SQX_144_Full\user\extend\CustomAnalysis\models\
      3. Los .java fuente de QlibSignal (OnnxModelManager, QlibSignal,
         QlibSignalCore) -> C:\SQX_144_Full\user\extend\Snippets\SQ\
         TALibIndicators\QlibSignal\ (fuente, NO los .class compilados --
         el Code Editor real de SQX debe compilarlos el mismo, con su propio
         Log/SettingsMap reales, no con los stubs usados para desarrollo
         local. Copiar .class compilados aqui NO tiene sentido y podria
         confundir al classloader de snippets de SQX).

.NOTES
    ADVERTENCIA IMPORTANTE (léase antes de correr):
    - model.onnx + feature_spec.json son de un modelo de PRUEBA (datos
      sintéticos, LightGBM directo -- ver Qlib_ONNX_Bridge_Design.md, Tarea
      T2). Confirmar que este es realmente el artefacto que se quiere
      desplegar antes de correr esto, no asumir que ya es el modelo Qlib
      real entrenado sobre datos de mercado reales.
    - Pendiente sin verificar (TODOS.md, sub-punto de P1): la interacción
      del jar de onnxruntime con el classloader custom de snippets de SQX
      (extracción de DLL nativa, hot-reload). Este script NO reinicia
      StrategyQuantX.exe -- eso queda a criterio del usuario, ya que
      reiniciar la app viva interrumpe backtests/monitoreo en curso.
    - Los gates (b)/(c) de /plan-ceo-review (fuga temporal, paridad de
      fuente de datos Qlib vs SQX real) siguen sin correr contra datos
      reales -- ver Qlib_ONNX_Bridge_Design.md.

.EXAMPLE
    # Revisar en modo dry-run primero (no copia nada, solo muestra qué haría):
    .\deploy_to_sqx.ps1 -DryRun

    # Ejecutar de verdad:
    .\deploy_to_sqx.ps1
#>
param(
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$ProjectRoot = "E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT"
$SqxRoot     = "C:\SQX_144_Full"

$Copies = @(
    @{
        What = "onnxruntime jar"
        Src  = Join-Path $ProjectRoot "spike\lib\onnxruntime-1.29.0.jar"
        Dst  = Join-Path $SqxRoot "user\libs\onnxruntime-1.29.0.jar"
    },
    @{
        What = "model.onnx (modelo de PRUEBA, sintetico)"
        Src  = Join-Path $ProjectRoot "qlib_export\output\model.onnx"
        Dst  = Join-Path $SqxRoot "user\extend\CustomAnalysis\models\model.onnx"
    },
    @{
        What = "feature_spec.json (modelo de PRUEBA, sintetico)"
        Src  = Join-Path $ProjectRoot "qlib_export\output\feature_spec.json"
        Dst  = Join-Path $SqxRoot "user\extend\CustomAnalysis\models\feature_spec.json"
    },
    @{
        What = "OnnxModelManager.java (fuente, NO compilado -- el Code Editor real compila)"
        Src  = Join-Path $ProjectRoot "user\extend\Snippets\SQ\TALibIndicators\QlibSignal\OnnxModelManager.java"
        Dst  = Join-Path $SqxRoot "user\extend\Snippets\SQ\TALibIndicators\QlibSignal\OnnxModelManager.java"
    },
    @{
        What = "QlibSignalCore.java (fuente)"
        Src  = Join-Path $ProjectRoot "user\extend\Snippets\SQ\TALibIndicators\QlibSignal\QlibSignalCore.java"
        Dst  = Join-Path $SqxRoot "user\extend\Snippets\SQ\TALibIndicators\QlibSignal\QlibSignalCore.java"
    },
    @{
        What = "QlibSignal.java (fuente)"
        Src  = Join-Path $ProjectRoot "user\extend\Snippets\SQ\TALibIndicators\QlibSignal\QlibSignal.java"
        Dst  = Join-Path $SqxRoot "user\extend\Snippets\SQ\TALibIndicators\QlibSignal\QlibSignal.java"
    }
)

Write-Host "=== Despliegue Qlib->ONNX->SQX (Fase 3, Tarea T5) ===" -ForegroundColor Cyan
Write-Host "Origen:  $ProjectRoot"
Write-Host "Destino: $SqxRoot (instalacion VIVA)"
Write-Host ""

foreach ($c in $Copies) {
    if (-not (Test-Path -LiteralPath $c.Src)) {
        Write-Host "FALTA: $($c.What) -- no existe en $($c.Src)" -ForegroundColor Red
        continue
    }

    $dstDir = Split-Path -Parent $c.Dst
    if ($DryRun) {
        Write-Host "[DRY-RUN] Copiaria: $($c.What)"
        Write-Host "          $($c.Src)"
        Write-Host "       -> $($c.Dst)"
        if (-not (Test-Path -LiteralPath $dstDir)) {
            Write-Host "          (creando directorio destino: $dstDir)"
        }
    } else {
        if (-not (Test-Path -LiteralPath $dstDir)) {
            New-Item -ItemType Directory -Force -Path $dstDir | Out-Null
        }
        Copy-Item -LiteralPath $c.Src -Destination $c.Dst -Force
        Write-Host "OK: $($c.What) copiado a $($c.Dst)" -ForegroundColor Green
    }
}

Write-Host ""
if ($DryRun) {
    Write-Host "Dry-run completo -- nada se copio. Correr sin -DryRun para desplegar de verdad." -ForegroundColor Yellow
} else {
    Write-Host "Despliegue completo." -ForegroundColor Green
    Write-Host ""
    Write-Host "SIGUIENTES PASOS MANUALES (no automatizados por este script):" -ForegroundColor Cyan
    Write-Host "  1. (Verificado 2026-08-13: --enable-native-access=ALL-UNNAMED YA estaba en"
    Write-Host "     StrategyQuantX.config y CodeEditor.config -- nada que agregar aqui.)"
    Write-Host "  2. Reiniciar StrategyQuantX.exe para que recoja el jar nuevo en user\libs\."
    Write-Host "  3. Abrir el Code Editor real de SQX y compilar QlibSignal/OnnxModelManager/"
    Write-Host "     QlibSignalCore ahi -- valida la interaccion con el classloader real de"
    Write-Host "     snippets, que este despliegue NO puede probar (TODOS.md, sub-punto de P1)."
    Write-Host "  4. Confirmar visualmente que SQX arranca limpio (mismo procedimiento que"
    Write-Host "     incidentes previos de snippets, ver ClaudeCode_SQX_Notes.md)."
}
