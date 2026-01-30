$PSScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $PSScriptRoot
$venvName = "venv"
$venvPython = Join-Path $PSScriptRoot "$venvName\Scripts\python.exe"
$script = "main.py"

if (-not (Test-Path "$venvPython")) {
    Write-Host "Venv not found. Running setup..." -ForegroundColor Yellow
    .\install.ps1   
}
Write-Host "Activating environment and running $script..." -ForegroundColor Cyan
 & $venvPython $script 
 
Write-Host "`nPress any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")