$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot

& "$projectRoot\.venv\Scripts\python.exe" `
    "$projectRoot\tools\device-to-glb.py" `
    --id crac-liebert-crv `
    --width 300 `
    --depth 1132 `
    --height 2000 `
    --front "$projectRoot\ref\liebert-crac\prepared\front.png" `
    --color "#1f1f1f" `
    --output "$projectRoot\models\crac-liebert-crv.glb"