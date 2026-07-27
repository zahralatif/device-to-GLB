$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot

& "$projectRoot\.venv\Scripts\python.exe" `
    "$projectRoot\tools\device-to-glb.py" `
    --id ups-3u-apc-smart-ups-xl-sua3000rmxl3u `
    --width 443 `
    --depth 660 `
    --height 132 `
    --front "$projectRoot\ref\ups-3u-apc-smart-ups-xl-sua3000rmxl3u\prepared\front.png" `
    --rear "$projectRoot\ref\ups-3u-apc-smart-ups-xl-sua3000rmxl3u\prepared\rear.png" `
    --color "#1a1a1a" `
    --output "$projectRoot\models\ups-3u-apc-smart-ups-xl-sua3000rmxl3u.glb" `
    --manifest "$projectRoot\manifest.json"