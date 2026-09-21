$ErrorActionPreference = 'Stop'

$workspaceRoot = 'E:\PROYECTOS\CLAUDE CODE\STRATEGY QUANT'
$liveRoot = 'C:\SQX_144_Full'

$sourceFile = Join-Path $workspaceRoot 'user\extend\Snippets\SQ\Columns\Databanks\PropFirmComplianceLogic.java'
$targetFile = Join-Path $liveRoot 'user\extend\Snippets\SQ\Columns\Databanks\PropFirmComplianceLogic.java'
$targetDir = Split-Path $targetFile -Parent

if (-not (Test-Path $sourceFile)) {
    throw "No existe la fuente correcta: $sourceFile"
}

New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
Copy-Item -Force -LiteralPath $sourceFile -Destination $targetFile

$content = Get-Content -LiteralPath $targetFile -Raw
if ($content -notmatch '^package\s+SQ\.Columns\.Databanks;') {
    $content = $content -replace '^package\s+.*?;', 'package SQ.Columns.Databanks;'
    Set-Content -LiteralPath $targetFile -Value $content -Encoding UTF8
}

$staleClassDirs = @(
    (Join-Path $liveRoot 'user\extend\Snippets\SQ\Columns\Databanks'),
    (Join-Path $liveRoot 'user\extend\Snippets\SQ\Conditions\PropFirm'),
    (Join-Path $liveRoot 'user\extend\Snippets\SQ\Indicators\bin')
)

foreach ($dir in $staleClassDirs) {
    if (Test-Path $dir) {
        Get-ChildItem -Path $dir -Recurse -Filter *.class -File -ErrorAction SilentlyContinue | ForEach-Object {
            Remove-Item -LiteralPath $_.FullName -Force
        }
    }
}

$javaFiles = Get-ChildItem -Path (Join-Path $liveRoot 'user\extend\Snippets') -Recurse -Filter *.java -File -ErrorAction SilentlyContinue
foreach ($file in $javaFiles) {
    $file.LastWriteTime = Get-Date
}

Write-Host "Reparación aplicada."
Write-Host "Fuente: $sourceFile"
Write-Host "Destino: $targetFile"
Write-Host "Paquete verificado: package SQ.Columns.Databanks;"
Write-Host "Clase .class stale eliminada y timestamps refrescados."
