# Install api-platform-skills for Claude Code and other agents (Windows).
[CmdletBinding()]
param(
    [switch]$Project,
    [switch]$Claude,
    [switch]$All,
    [switch]$Clean,
    [switch]$Help
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$Root = [System.IO.Path]::GetFullPath((Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) ".."))
$Src = Join-Path $Root "skills"
$UserHome = if ([string]::IsNullOrWhiteSpace($env:USERPROFILE)) { $HOME } else { $env:USERPROFILE }

function Normalize-Path([string]$Path) {
    $full = [System.IO.Path]::GetFullPath($Path)
    $root = [System.IO.Path]::GetPathRoot($full)
    if ($full -eq $root) { return $root }
    return $full.TrimEnd([char[]]'\/')
}

function Show-Usage {
    @"
Usage: install.ps1 [-Claude] [-Project] [-All] [-Clean]

  -Claude  Install to the current user's .claude\skills directory (the default)
  -Project Install to the current project's agent skill directories
  -All     Install to Claude, .agents, and .cursor user directories
  -Clean   Remove each existing package skill directory before copying
"@
}

function Test-SameOrChild([string]$Candidate, [string]$Parent) {
    $candidatePath = Normalize-Path $Candidate
    $parentPath = Normalize-Path $Parent
    return $candidatePath.Equals($parentPath, [System.StringComparison]::OrdinalIgnoreCase) -or
        $candidatePath.StartsWith($parentPath + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase) -or
        $candidatePath.StartsWith($parentPath + [System.IO.Path]::AltDirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)
}

function Test-ReparsePoint($Item) {
    $linkProperty = $Item.PSObject.Properties['LinkType']
    if ($null -ne $linkProperty -and -not [string]::IsNullOrWhiteSpace([string]$Item.LinkType)) {
        return $true
    }
    return (($Item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0)
}

function Assert-Destination([string]$Dest) {
    $full = Normalize-Path $Dest
    if ($full -eq [System.IO.Path]::GetPathRoot($full)) {
        throw "Refusing to install into a filesystem root: $Dest"
    }
    if (Test-SameOrChild $full $Src) {
        throw "Refusing to install into the source tree: $Dest"
    }
    if (Test-Path -LiteralPath $Dest) {
        $item = Get-Item -LiteralPath $Dest -Force
        if (Test-ReparsePoint $item) {
            throw "Refusing to install through a symlink or junction: $Dest"
        }
        if (-not $item.PSIsContainer) {
            throw "Destination exists as a file: $Dest"
        }
    }
}

function Assert-NoLinkAncestors([string]$Dest) {
    $current = Normalize-Path $Dest
    while ($true) {
        if (Test-Path -LiteralPath $current) {
            $item = Get-Item -LiteralPath $current -Force
            if (Test-ReparsePoint $item) {
                throw "Refusing to install through a symlink or junction: $current"
            }
        }
        $parent = [System.IO.Path]::GetDirectoryName($current)
        if ([string]::IsNullOrWhiteSpace($parent) -or $parent -eq $current) { break }
        $current = Normalize-Path $parent
    }
}

function Assert-NoLinks([string]$Path) {
    $items = @(Get-Item -LiteralPath $Path -Force) + @(Get-ChildItem -LiteralPath $Path -Force -Recurse)
    foreach ($item in $items) {
        if (Test-ReparsePoint $item) {
            throw "Refusing to write through a symlink or junction: $($item.FullName)"
        }
    }
}

function Copy-Skills([string]$Dest) {
    Assert-Destination $Dest
    Assert-NoLinkAncestors $Dest
    New-Item -ItemType Directory -Force -Path $Dest | Out-Null
    $skillSources = Get-ChildItem -LiteralPath $Src -Directory -Force | Sort-Object Name
    foreach ($source in $skillSources) {
        $target = Join-Path $Dest $source.Name
        if (Test-Path -LiteralPath $target) {
            $existing = Get-Item -LiteralPath $target -Force
            if (Test-ReparsePoint $existing) {
                throw "Refusing to write through a symlink or junction: $target"
            }
            if (-not $existing.PSIsContainer) {
                throw "Skill destination exists as a file: $target"
            }
            if ($Clean) {
                Remove-Item -LiteralPath $target -Recurse -Force
            } else {
                Assert-NoLinks $target
            }
        }
        New-Item -ItemType Directory -Force -Path $target | Out-Null
        Get-ChildItem -LiteralPath $source.FullName -Force | ForEach-Object {
            Copy-Item -LiteralPath $_.FullName -Destination $target -Recurse -Force
        }
        Write-Host "  + $($source.Name) -> $target"
    }
}

if ($Help) {
    Show-Usage
    exit 0
}
if (-not (Test-Path -LiteralPath $Src -PathType Container)) {
    throw "skills/ not found at $Src"
}
if (-not $Project -and -not $Claude -and -not $All) {
    $Claude = $true
}

Write-Host "api-platform-skills installer"
Write-Host "source: $Src"
if ($Clean) {
    Write-Host "Clean mode: existing package skill directories will be removed before copying."
}

if ($Claude -or $All) {
    $dest = Join-Path $UserHome ".claude\skills"
    Write-Host "mode: Claude Code user skills"
    Write-Host "-> $dest"
    Copy-Skills $dest
}

if ($All) {
    Write-Host "mode: all user harnesses"
    foreach ($rel in @(".agents\skills", ".cursor\skills")) {
        $dest = Join-Path $UserHome $rel
        Write-Host "-> $dest"
        Copy-Skills $dest
    }
}

if ($Project) {
    $base = (Get-Location).Path
    Write-Host "mode: project ($base)"
    foreach ($rel in @(".claude\skills", ".agents\skills", ".cursor\skills", ".github\skills")) {
        $dest = Join-Path $base $rel
        Write-Host "-> $dest"
        Copy-Skills $dest
    }
}

Write-Host ""
Write-Host "Done."
Write-Host "Claude Code: restart the session (or /reload-plugins if using plugin install)."
Write-Host "Try: Review openapi.v1 vs openapi.v2-bad with breaking-change-review"
