param(
    [Parameter(Mandatory = $true)]
    [string]$DatabankDir,

    [Parameter(Mandatory = $true)]
    [string]$StatsCsv,

    [Parameter(Mandatory = $true)]
    [double]$Threshold,

    [Parameter(Mandatory = $true)]
    [string]$SurvivorsFile
)

$ErrorActionPreference = 'Stop'

$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$SqxRoot = 'C:\SQX_144_Full'
$JavaExe = Join-Path $SqxRoot 'j64\bin\java.exe'
$RobustnessDir = Join-Path $ScriptRoot 'user\extend\CustomAnalysis\RobustnessFilter'
$Classpath = @(
    '.'
    (Join-Path $SqxRoot 'internal\libs\*')
    $RobustnessDir
) -join ';'

foreach ($path in @($DatabankDir, $StatsCsv)) {
    if (-not (Test-Path $path)) {
        throw "Path not found: $path"
    }
}

if (-not (Test-Path $JavaExe)) {
    throw "Java executable not found: $JavaExe"
}

Write-Host "Running BatchRobustness..."
& $JavaExe '-cp' $Classpath 'BatchRobustness' $DatabankDir $StatsCsv
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host "Running CorrelationFilterSim..."
& $JavaExe '-cp' $Classpath 'CorrelationFilterSim' 'project' $DatabankDir $StatsCsv $Threshold $SurvivorsFile
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host "Done. Survivors written to: $SurvivorsFile"
