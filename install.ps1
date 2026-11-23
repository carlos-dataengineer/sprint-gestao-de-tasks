<#
.SYNOPSIS
  Instala a Sprint - Gestao de Tasks: a skill para Claude e Codex, e a ferramenta pronta no computador.

.DESCRIPTION
  1. Baixa a Sprint do GitHub (ou usa a pasta local, se rodar de um clone).
  2. Instala a skill "sprint" em:
       ~/.claude/skills/sprint      (Claude Code e app desktop do Claude)
       ~/.codex/skills/sprint       (Codex; respeita CODEX_HOME)
       ~/.agents/skills/sprint      (pasta de skills compartilhada entre agentes)
  3. Gera a ferramenta em ~/Sprint/Sprint.html e abre no navegador.

.EXAMPLE
  irm https://raw.githubusercontent.com/carlos-dataengineer/sprint-gestao-de-tasks/main/install.ps1 | iex

.EXAMPLE
  .\install.ps1 -NoOpen -SkipCodex

.NOTES
  Quando rodar via "irm | iex", use variaveis de ambiente no lugar dos parametros:
    $env:SPRINT_NO_OPEN = '1'; $env:SPRINT_SKIP_CODEX = '1'; $env:SPRINT_SKIP_CLAUDE = '1'; $env:SPRINT_REF = 'v2.0.0'
#>
[CmdletBinding()]
param(
  [switch]$NoOpen,
  [switch]$SkipClaude,
  [switch]$SkipCodex,
  [string]$Ref = ''
)

$ErrorActionPreference = 'Stop'
$Repo = 'carlos-dataengineer/sprint-gestao-de-tasks'
$SkillName = 'sprint'
$LegacyNames = @('sprint-task-management')

if ($env:SPRINT_NO_OPEN -eq '1') { $NoOpen = $true }
if ($env:SPRINT_SKIP_CLAUDE -eq '1') { $SkipClaude = $true }
if ($env:SPRINT_SKIP_CODEX -eq '1') { $SkipCodex = $true }
if (-not $Ref) { $Ref = if ($env:SPRINT_REF) { $env:SPRINT_REF } else { 'main' } }

function Write-Step([string]$Text) { Write-Host "  > $Text" -ForegroundColor Cyan }
function Write-Ok([string]$Text) { Write-Host "  ok $Text" -ForegroundColor Green }

Write-Host ''
Write-Host '  Sprint - Gestao de Tasks' -ForegroundColor White
Write-Host '  cronograma de sprints + quadro Kanban + saude do projeto' -ForegroundColor DarkGray
Write-Host ''

# 1. Origem dos arquivos ------------------------------------------------------
$temp = $null
$localRoot = if ($PSScriptRoot) { $PSScriptRoot } else { $null }
if ($localRoot -and (Test-Path (Join-Path $localRoot 'skills/sprint/SKILL.md'))) {
  $root = $localRoot
  Write-Step "Usando os arquivos locais em $root"
} else {
  try { [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12 } catch {}
  $temp = Join-Path ([IO.Path]::GetTempPath()) ("sprint-" + [guid]::NewGuid().ToString('N'))
  New-Item -ItemType Directory -Path $temp | Out-Null
  $zip = Join-Path $temp 'sprint.zip'
  $kind = if ($Ref -match '^v\d') { 'tags' } else { 'heads' }
  $url = "https://codeload.github.com/$Repo/zip/refs/$kind/$Ref"
  Write-Step "Baixando $Repo ($Ref)"
  Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing
  Expand-Archive -Path $zip -DestinationPath $temp -Force
  $root = Get-ChildItem -Path $temp -Directory | Where-Object { Test-Path (Join-Path $_.FullName 'skills/sprint/SKILL.md') } | Select-Object -First 1 -ExpandProperty FullName
  if (-not $root) { throw 'O pacote baixado nao tem skills/sprint/SKILL.md.' }
}
$skillSrc = Join-Path $root 'skills/sprint'

# 2. Skill ------------------------------------------------------------------
function Test-SkillName([string]$Dir, [string]$Name) {
  $manifest = Join-Path $Dir 'SKILL.md'
  if (-not (Test-Path $manifest)) { return $false }
  return ((Get-Content $manifest -Raw -Encoding UTF8) -match "(?m)^name:\s*$([regex]::Escape($Name))\s*$")
}

function Install-Skill([string]$SkillsDir, [string]$Label) {
  foreach ($old in $LegacyNames) {
    $legacy = Join-Path $SkillsDir $old
    if ((Test-Path $legacy) -and (Test-SkillName $legacy $old)) {
      Remove-Item -Path $legacy -Recurse -Force
      Write-Ok "Versao antiga removida de $legacy"
    }
  }
  $target = Join-Path $SkillsDir $SkillName
  if (Test-Path $target) {
    if (-not (Test-SkillName $target $SkillName)) {
      Write-Warning "$target ja existe e nao parece ser a Sprint. Pulei $Label para nao apagar nada."
      return
    }
    Remove-Item -Path $target -Recurse -Force
  }
  New-Item -ItemType Directory -Path $SkillsDir -Force | Out-Null
  Copy-Item -Path $skillSrc -Destination $target -Recurse -Force
  Write-Ok "Skill instalada para $Label em $target"
}

$installed = @()
if (-not $SkipClaude) {
  Install-Skill (Join-Path $HOME '.claude/skills') 'Claude'
  $installed += 'Claude'
}
if (-not $SkipCodex) {
  $codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
  Install-Skill (Join-Path $codexHome 'skills') 'Codex'
  Install-Skill (Join-Path $HOME '.agents/skills') 'agentes (pasta compartilhada)'
  $installed += 'Codex'
}

# 3. Ferramenta pronta ---------------------------------------------------------
$appDir = Join-Path $HOME 'Sprint'
New-Item -ItemType Directory -Path $appDir -Force | Out-Null
$appFile = Join-Path $appDir 'Sprint.html'
Copy-Item -Path (Join-Path $skillSrc 'assets/sprint.html') -Destination $appFile -Force
Write-Ok "Ferramenta gerada em $appFile"

if (-not $NoOpen) {
  try { Start-Process $appFile; Write-Ok 'Aberta no navegador' } catch { Write-Warning "Nao consegui abrir o navegador. Abra manualmente: $appFile" }
}

if ($temp) { Remove-Item -Path $temp -Recurse -Force -ErrorAction SilentlyContinue }

# 4. Proximos passos --------------------------------------------------------------
Write-Host ''
Write-Host '  Pronto. Como usar:' -ForegroundColor White
Write-Host "    Navegador  $appFile  (modo local, ja com um projeto de exemplo)"
if ($installed -contains 'Claude') { Write-Host '    Claude     digite /sprint ou peca "abra a Sprint": vira um artefato compartilhado' }
if ($installed -contains 'Codex') { Write-Host '    Codex      digite $sprint ou peca "abra a Sprint"' }
Write-Host ''
Write-Host '  Abra uma nova conversa para o agente reconhecer a skill.' -ForegroundColor DarkGray
Write-Host ''
