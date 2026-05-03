param(
    [Parameter(Mandatory = $true)]
    [string] $OutPrefix
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$Destination = Join-Path (Split-Path -Parent $RepoRoot) "$OutPrefix.zip"

$ExcludeDir = @(".venv", ".pytest_cache", ".mypy_cache", "__pycache__", "node_modules")

$Selections = Get-ChildItem -LiteralPath $RepoRoot -Force | Where-Object {
    if (-not $_.PSIsContainer) { return $true }
    return $ExcludeDir -notcontains $_.Name
}

if (Test-Path $Destination) {
    Remove-Item -Force $Destination
}

Compress-Archive -LiteralPath ($Selections.FullName) -DestinationPath $Destination -CompressionLevel Optimal -Force

Write-Host "Wrote:" $Destination
