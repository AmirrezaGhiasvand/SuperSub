param([string]$Python = 'python')
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
function Invoke-Checked {
    param([string]$Executable, [string[]]$Arguments)
    & $Executable @Arguments
    if ($LASTEXITCODE -ne 0) { throw "Setup failed: $Executable $($Arguments -join ' ')" }
}
if (!(Test-Path '.venv/Scripts/python.exe')) {
    if (!(Get-Command $Python -ErrorAction SilentlyContinue)) { throw 'Install 64-bit Python 3.11+ from python.org, enable Add Python to PATH, reopen this window and retry.' }
    Invoke-Checked $Python @('-c', 'import sys; assert sys.version_info >= (3,11); assert sys.maxsize > 2**32')
    Invoke-Checked $Python @('-m', 'venv', '.venv')
}
$venvPython = Join-Path $PSScriptRoot '.venv/Scripts/python.exe'
Invoke-Checked $venvPython @('-m', 'pip', 'install', '-r', 'requirements.txt')
New-Item -ItemType Directory -Force assets, models, data | Out-Null
Invoke-Checked $venvPython @('-c', 'import app, faster_whisper')
Write-Host 'Setup complete. Double-click Start.cmd to launch SuperSub.'
