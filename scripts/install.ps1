# Install api-platform-skills into common agent skill directories (Windows).
param(
    [switch]$Project
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Src = Join-Path $Root "skills"

function Copy-Skills([string]$Dest) {
    New-Item -ItemType Directory -Force -Path $Dest | Out-Null
    Get-ChildItem -Directory $Src | ForEach-Object {
        $target = Join-Path $Dest $_.Name
        if (Test-Path $target) { Remove-Item -Recurse -Force $target }
        Copy-Item -Recurse $_.FullName $target
        Write-Host "  + $($_.Name) -> $target"
    }
}

Write-Host "api-platform-skills installer"
Write-Host "source: $Src"

if ($Project) {
    $Base = (Get-Location).Path
    Write-Host "mode: project ($Base)"
    foreach ($rel in @(".agents\skills", ".claude\skills", ".cursor\skills", ".github\skills")) {
        $dest = Join-Path $Base $rel
        Write-Host "-> $dest"
        Copy-Skills $dest
    }
} else {
    Write-Host "mode: user"
    $home = $env:USERPROFILE
    foreach ($rel in @(".agents\skills", ".claude\skills", ".cursor\skills")) {
        $dest = Join-Path $home $rel
        Write-Host "-> $dest"
        Copy-Skills $dest
    }
}

Write-Host "Done. Restart or re-index your agent if skills do not appear."
