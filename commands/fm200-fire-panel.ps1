$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot

& "$projectRoot\.venv\Scripts\python.exe" `
    "$projectRoot\tools\device-to-glb.py" `
    --id fm200-fire-panel `
    --width 540 `
    --depth 140 `
    --height 400 `
    --front "$projectRoot\ref\fm200-fire-panel\prepared\front.png" `
    --color "#861212" `
    --output "$projectRoot\models\fm200-fire-panel.glb" `
    --manifest "$projectRoot\manifest.json"