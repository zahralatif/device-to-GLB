$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot

& "$projectRoot\.venv\Scripts\python.exe" `
    "$projectRoot\tools\device-to-glb-hq.py" `
    --id pdu-0u-vertiv-geist-rpdu-30-outlet `
    --width 50 `
    --depth 60 `
    --height 1700 `
    --front "$projectRoot\ref\pdu-0u-vertiv-geist-rpdu-30-outlet\prepared\front.png" `
    --color "#a3a3a3" `
    --bevel 1.0 `
    --output "$projectRoot\models\pdu-0u-vertiv-geist-rpdu-30-outlet.glb" `
    --manifest "$projectRoot\manifest.json"