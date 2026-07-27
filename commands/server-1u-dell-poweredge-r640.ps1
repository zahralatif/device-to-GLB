$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot

& "$projectRoot\.venv\Scripts\python.exe" `
    "$projectRoot\tools\device-to-glb-hq.py" `
    --id server-1u-dell-poweredge-r640 `
    --width 443 `
    --depth 734 `
    --height 43 `
    --front "$projectRoot\ref\server-1u-dell-poweredge-r640\prepared\front.png" `
    --rear "$projectRoot\ref\server-1u-dell-poweredge-r640\prepared\rear.png" `
    --color "#2d2d2d" `
    --bevel 1.5 `
    --output "$projectRoot\models\server-1u-dell-poweredge-r640.glb" `
    --manifest "$projectRoot\manifest.json"