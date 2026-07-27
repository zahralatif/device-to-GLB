$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot

& "$projectRoot\.venv\Scripts\python.exe" `
    "$projectRoot\tools\device-to-glb.py" `
    --id switch-1u-cisco-9300 `
    --width 445 `
    --depth 483 `
    --height 44 `
    --front "$projectRoot\ref\cisco-9300\prepared\front.png" `
    --rear "$projectRoot\ref\cisco-9300\prepared\rear.png" `
    --color "#1a1a2e" `
    --output "$projectRoot\models\switch-1u-cisco-9300.glb" `
    --manifest "$projectRoot\manifest.json"