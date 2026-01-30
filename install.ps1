$venv = "venv"

Write-Host "Creating venv..." -ForegroundColor Cyan
python -m venv $venv

$venvPython= Join-Path (Get-Location) "$venv\Scripts\python.exe"

if (Test-Path "requirements.txt") {
    Write-Host "Installing dependencies..." -ForegroundColor Cyan
    & $venvPython -m pip install --upgrade pip
    & $venvPython -m pip install -r requirements.txt
    Write-Host "Done!" -ForegroundColor Green
} else {
    Write-Host "requirements.txt not found, skipping install." -ForegroundColor Yellow
}