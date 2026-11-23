<#
.SYNOPSIS
  Remove a skill da Sprint do Claude e do Codex.
.DESCRIPTION
  Apaga apenas pastas cujo SKILL.md se chama "sprint" (ou o nome antigo "sprint-task-management").
  A ferramenta em ~/Sprint fica, a menos que voce use -All. As tasks salvas no navegador e
  os artefatos publicados no Claude nao sao tocados.
.EXAMPLE
  irm https://raw.githubusercontent.com/carlos-dataengineer/sprint-gestao-de-tasks/main/uninstall.ps1 | iex
.EXAMPLE
  .\uninstall.ps1 -All
#>
[CmdletBinding()]
param([switch]$All)
$ErrorActionPreference = 'Stop'
if ($env:SPRINT_UNINSTALL_ALL -eq '1') { $All = $true }

$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$dirs = @((Join-Path $HOME '.claude/skills'), (Join-Path $codexHome 'skills'), (Join-Path $HOME '.agents/skills'))
foreach ($d in $dirs) {
  foreach ($name in @('sprint', 'sprint-task-management')) {
    $t = Join-Path $d $name
    $m = Join-Path $t 'SKILL.md'
    if ((Test-Path $m) -and ((Get-Content $m -Raw -Encoding UTF8) -match "(?m)^name:\s*$([regex]::Escape($name))\s*$")) {
      Remove-Item -Path $t -Recurse -Force
      Write-Host "  removido: $t"
    }
  }
}
$app = Join-Path $HOME 'Sprint/Sprint.html'
if ($All -and (Test-Path $app)) {
  Remove-Item -Path $app -Force
  $dir = Split-Path $app -Parent
  if (-not (Get-ChildItem -Path $dir -Force)) { Remove-Item -Path $dir -Force }
  Write-Host "  removido: $app"
} elseif (Test-Path $app) {
  Write-Host "  mantido: $app (use -All para remover)"
}
Write-Host '  Sprint desinstalada.'
