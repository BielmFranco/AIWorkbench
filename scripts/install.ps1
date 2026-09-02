[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("codex", "claude")]
    [string]$Target,
    [string]$Skill = "all",
    [string]$InstallPath
)

$ErrorActionPreference = "Stop"
$repositoryRoot = Split-Path -Parent $PSScriptRoot
$sourceRoot = Join-Path $repositoryRoot "skills"

if (-not (Test-Path -LiteralPath $sourceRoot -PathType Container)) {
    throw "Skills directory not found: $sourceRoot"
}

if ($Target -eq "codex") {
    $codexRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
    $destinationRoot = Join-Path $codexRoot "skills"
} else {
    $destinationRoot = Join-Path (Join-Path $HOME ".claude") "skills"
}
if ($InstallPath) {
    $destinationRoot = $InstallPath
}

$sources = if ($Skill -eq "all") {
    Get-ChildItem -LiteralPath $sourceRoot -Directory
} else {
    $selected = Join-Path $sourceRoot $Skill
    if (-not (Test-Path -LiteralPath (Join-Path $selected "SKILL.md") -PathType Leaf)) {
        throw "Unknown skill: $Skill"
    }
    @(Get-Item -LiteralPath $selected)
}

New-Item -ItemType Directory -Force -Path $destinationRoot | Out-Null
foreach ($source in $sources) {
    $destination = Join-Path $destinationRoot $source.Name
    New-Item -ItemType Directory -Force -Path $destination | Out-Null
    Get-ChildItem -LiteralPath $source.FullName -Force |
        Copy-Item -Destination $destination -Recurse -Force
    Write-Host "Installed: $($source.Name) -> $destination"
}

Write-Host "Done: $($sources.Count) skill(s) installed for $Target."
