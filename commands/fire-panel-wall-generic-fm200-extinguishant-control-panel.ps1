$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot

& "$projectRoot\.venv\Scripts\python.exe" `
    "$projectRoot\tools\device-to-glb-hq.py" `
    --id fire-panel-wall-generic-fm200-extinguishant-control-panel `
    --width 540 `
    --depth 140 `
    --height 400 `
    --front "$projectRoot\ref\fire-panel-wall-generic-fm200-extinguishant-control-panel\prepared\front.png" `
    --color "#861212" `
    --output "$projectRoot\models\fire-panel-wall-generic-fm200-extinguishant-control-panel.glb" `
    --manifest "$projectRoot\manifest.json"