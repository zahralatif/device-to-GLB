$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot

& "$projectRoot\.venv\Scripts\python.exe" `
    "$projectRoot\tools\device-to-glb.py" `
    --id server-1u-generic `
    --width 443 `
    --depth 734 `
    --height 43 `
    --front "$projectRoot\ref\server-1u\prepared\front.png" `
    --rear "$projectRoot\ref\server-1u\prepared\rear.png" `
    --color "#2d2d2d" `
    --output "$projectRoot\models\server-1u-generic.glb" `
    --manifest "$projectRoot\manifest.json"