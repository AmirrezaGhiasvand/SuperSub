param([int]$Port = 8765, [switch]$NoBrowser)
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$python = Join-Path $PSScriptRoot '.venv/Scripts/python.exe'
if (!(Test-Path $python)) { throw 'Run Setup.cmd first.' }
& $python -c 'import fastapi, uvicorn, faster_whisper'
if ($LASTEXITCODE -ne 0) { throw 'Dependencies missing. Run Setup.cmd again.' }
if (!$NoBrowser) {
    $url = "http://127.0.0.1:$Port"
    Start-Job -ArgumentList $url -ScriptBlock {
        param($url)
        for ($i = 0; $i -lt 60; $i++) {
            try { Invoke-WebRequest "$url/api/models" -UseBasicParsing | Out-Null; Start-Process $url; return } catch { Start-Sleep -Seconds 1 }
        }
    } | Out-Null
}
& $python -m uvicorn app:app --host 127.0.0.1 --port $Port
if ($LASTEXITCODE -ne 0) { throw 'SuperSub could not start. Check the port and error above.' }
