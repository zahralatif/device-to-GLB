$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot

& "$projectRoot\.venv\Scripts\python.exe" `
    "$projectRoot\tools\device-to-glb-hq.py" `
    --id switch-1u-cisco-catalyst-c9300-48p-m `
    --width 445 `
    --depth 483 `
    --height 44 `
    --front "$projectRoot\ref\switch-1u-cisco-catalyst-c9300-48p-m\prepared\front.png" `
    --rear "$projectRoot\ref\switch-1u-cisco-catalyst-c9300-48p-m\prepared\rear.png" `
    --color "#1a1a2e" `
    --output "$projectRoot\models\switch-1u-cisco-catalyst-c9300-48p-m.glb" `
    --manifest "$projectRoot\manifest.json"