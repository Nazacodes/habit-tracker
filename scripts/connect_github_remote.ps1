<#
.SYNOPSIS
  Point local git at a GitHub repo and print the push command.

  Create the repo on GitHub first (empty, no README), then run this script.

.PARAMETER GitHubUser
  Your GitHub username (the segment in github.com/<user>/...).

.PARAMETER RepoName
  Repository name (e.g. habit-studio or aisdlc).

.PARAMETER UseSsh
  If set, use git@github.com:... instead of https://...
#>
param(
    [Parameter(Mandatory = $true)]
    [string] $GitHubUser,

    [Parameter(Mandatory = $true)]
    [string] $RepoName,

    [switch] $UseSsh
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

if (-not (Test-Path .git)) {
    Write-Error "No .git folder here. Run from repo root or fix path."
    exit 1
}

$url = if ($UseSsh) {
    "git@github.com:${GitHubUser}/${RepoName}.git"
} else {
    "https://github.com/${GitHubUser}/${RepoName}.git"
}

$hasOrigin = $false
git remote get-url origin 2>$null | Out-Null
if ($LASTEXITCODE -eq 0) { $hasOrigin = $true }

if ($hasOrigin) {
    git remote set-url origin $url
    Write-Host "Updated remote origin -> $url"
} else {
    git remote add origin $url
    Write-Host "Added remote origin -> $url"
}

Write-Host ""
Write-Host "Next (after the empty repo exists on GitHub):"
Write-Host "  git push -u origin master"
Write-Host ""
Write-Host "If GitHub created default branch 'main' and you prefer it:"
Write-Host "  git branch -M main"
Write-Host "  git push -u origin main"
