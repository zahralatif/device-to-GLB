$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot

& "$projectRoot\.venv\Scripts\python.exe" `
    "$projectRoot\tools\device-to-glb-hq.py" `
    --id crac-floor-vertiv-liebert-crv `
    --width 1200 `
    --depth 800 `
    --height 1800 `
    --front "$projectRoot\ref\crac-floor-vertiv-liebert-crv\prepared\front.png" `
    --color "#252525" `
    --bevel 3.0 `
    --output "$projectRoot\models\crac-floor-vertiv-liebert-crv.glb" `
    --manifest "$projectRoot\manifest.json"