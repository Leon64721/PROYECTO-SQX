@echo off
SET executablePath=%~dp0StrategyQuantX.exe
reg add "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers" /v %executablePath% /t REG_SZ /d HIGHDPIAWARE /f
echo FIXING HIGH DPI FOR EXECUTABLE: %executablePath%

pause