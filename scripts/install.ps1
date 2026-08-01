# Install api-platform-skills for Claude Code and other agents (Windows).
param(
    [switch]$Project,
    [switch]$Claude,
    [switch]$All
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Src = Join-Path $Root "skills"

if (-not (Test-Path $Src)) {
    throw "skills/ not found at $Src"
}

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

# Default: Claude user skills (most common ask)
if (-not $Project -and -not $Claude -and -not $All) {
    $Claude = $true
}

if ($Claude -or $All) {
    $dest = Join-Path $env:USERPROFILE ".claude\skills"
    Write-Host "mode: Claude Code user skills"
    Write-Host "-> $dest"
    Copy-Skills $dest
}

if ($All) {
    Write-Host "mode: all user harnesses"
    foreach ($rel in @(".agents\skills", ".cursor\skills")) {
        $dest = Join-Path $env:USERPROFILE $rel
        Write-Host "-> $dest"
        Copy-Skills $dest
    }
}

if ($Project) {
    $Base = (Get-Location).Path
    Write-Host "mode: project ($Base)"
    foreach ($rel in @(".claude\skills", ".agents\skills", ".cursor\skills", ".github\skills")) {
        $dest = Join-Path $Base $rel
        Write-Host "-> $dest"
        Copy-Skills $dest
    }
}

Write-Host ""
Write-Host "Done."
Write-Host "Claude Code: restart the session (or /reload-plugins if using plugin install)."
Write-Host "Try: Review openapi.v1 vs openapi.v2-bad with breaking-change-review"
