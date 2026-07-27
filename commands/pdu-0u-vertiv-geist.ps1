$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot

& "$projectRoot\.venv\Scripts\python.exe" `
    "$projectRoot\tools\device-to-glb.py" `
    --id pdu-0u-vertiv-geist `
    --width 50 `
    --depth 60 `
    --height 1700 `
    --front "$projectRoot\ref\vertiv-pdu\prepared\front.png" `
    --color "#a3a3a3" `
    --output "$projectRoot\models\pdu-0u-vertiv-geist.glb" `
    --manifest "$projectRoot\manifest.json"