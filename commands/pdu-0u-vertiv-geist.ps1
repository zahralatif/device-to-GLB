$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot

& "$projectRoot\.venv\Scripts\python.exe" `
    "$projectRoot\tools\device-to-glb.py" `
    --id pdu-0u-vertiv-geist `
    --width 51 `
    --depth 51 `
    --height 1683 `
    --front "$projectRoot\ref\vertiv-pdu\prepared\front.png" `
    --color "#1a1a1a" `
    --output "$projectRoot\models\pdu-0u-vertiv-geist.glb"