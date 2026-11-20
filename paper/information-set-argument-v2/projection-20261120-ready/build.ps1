$ErrorActionPreference = 'Stop'
Push-Location -LiteralPath $PSScriptRoot
try {
    New-Item -ItemType Directory -Force -Path build | Out-Null
    foreach ($pass in 1..2) {
        & xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=build main.tex *> "build/pass$pass.txt"
        if ($LASTEXITCODE -ne 0) {
            Get-Content -LiteralPath "build/pass$pass.txt" -Tail 35
            throw "XeLaTeX failed on pass $pass."
        }
    }
    $problems = Select-String -LiteralPath 'build/main.log' -Pattern 'Overfull|Missing character|Undefined control sequence|LaTeX Font Warning|LaTeX Warning:.*undefined'
    if ($problems) {
        $problems | ForEach-Object { Write-Warning $_.Line }
        throw 'The compiled PDF needs review.'
    }
    Get-Item -LiteralPath 'build/main.pdf'
} finally {
    Pop-Location
}
