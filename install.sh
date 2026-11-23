#!/usr/bin/env bash
# Instala a Sprint — Gestão de Tasks: a skill para Claude e Codex, e a ferramenta pronta no computador.
#
#   curl -fsSL https://raw.githubusercontent.com/carlos-dataengineer/sprint-gestao-de-tasks/main/install.sh | bash
#
# Opções (também como variáveis de ambiente):
#   --no-open       não abre o navegador          SPRINT_NO_OPEN=1
#   --skip-claude   não instala no Claude         SPRINT_SKIP_CLAUDE=1
#   --skip-codex    não instala no Codex          SPRINT_SKIP_CODEX=1
#   --ref <ref>     branch ou tag (padrão: main)  SPRINT_REF=v2.0.0
set -euo pipefail

REPO="carlos-dataengineer/sprint-gestao-de-tasks"
SKILL_NAME="sprint"
LEGACY_NAMES="sprint-task-management"
NO_OPEN="${SPRINT_NO_OPEN:-0}"
SKIP_CLAUDE="${SPRINT_SKIP_CLAUDE:-0}"
SKIP_CODEX="${SPRINT_SKIP_CODEX:-0}"
REF="${SPRINT_REF:-main}"

while [ $# -gt 0 ]; do
  case "$1" in
    --no-open) NO_OPEN=1 ;;
    --skip-claude) SKIP_CLAUDE=1 ;;
    --skip-codex) SKIP_CODEX=1 ;;
    --ref) shift; REF="${1:?informe a branch ou tag}" ;;
    -h|--help) sed -n '2,11p' "$0"; exit 0 ;;
    *) echo "Opção desconhecida: $1" >&2; exit 1 ;;
  esac
  shift
done

step() { printf '  \033[36m>\033[0m %s\n' "$1"; }
ok()   { printf '  \033[32m✓\033[0m %s\n' "$1"; }
warn() { printf '  \033[33m!\033[0m %s\n' "$1" >&2; }

printf '\n  Sprint · Gestão de Tasks\n  cronograma de sprints + quadro Kanban + saúde do projeto\n\n'

# 1. Origem dos arquivos
TMP=""
cleanup() { if [ -n "$TMP" ]; then rm -rf "$TMP"; fi; }
trap cleanup EXIT

SCRIPT_DIR=""
if [ -n "${BASH_SOURCE[0]:-}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/skills/sprint/SKILL.md" ]; then
  ROOT="$SCRIPT_DIR"
  step "Usando os arquivos locais em $ROOT"
else
  command -v curl >/dev/null || { echo "Instale o curl e tente de novo." >&2; exit 1; }
  command -v tar >/dev/null || { echo "Instale o tar e tente de novo." >&2; exit 1; }
  TMP="$(mktemp -d)"
  case "$REF" in v[0-9]*) KIND="tags" ;; *) KIND="heads" ;; esac
  step "Baixando $REPO ($REF)"
  curl -fsSL "https://codeload.github.com/$REPO/tar.gz/refs/$KIND/$REF" | tar -xz -C "$TMP"
  ROOT="$(find "$TMP" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
  [ -f "$ROOT/skills/sprint/SKILL.md" ] || { echo "O pacote baixado não tem skills/sprint/SKILL.md." >&2; exit 1; }
fi
SKILL_SRC="$ROOT/skills/sprint"

# 2. Skill
has_name() { [ -f "$1/SKILL.md" ] && grep -Eq "^name:[[:space:]]*$2[[:space:]]*$" "$1/SKILL.md"; }

install_skill() {
  local dir="$1" label="$2" old target
  for old in $LEGACY_NAMES; do
    if [ -d "$dir/$old" ] && has_name "$dir/$old" "$old"; then
      rm -rf "${dir:?}/$old"
      ok "Versão antiga removida de $dir/$old"
    fi
  done
  target="$dir/$SKILL_NAME"
  if [ -e "$target" ]; then
    if has_name "$target" "$SKILL_NAME"; then
      rm -rf "$target"
    else
      warn "$target já existe e não parece ser a Sprint. Pulei $label para não apagar nada."
      return 0
    fi
  fi
  mkdir -p "$dir"
  cp -R "$SKILL_SRC" "$target"
  ok "Skill instalada para $label em $target"
}

INSTALLED=""
if [ "$SKIP_CLAUDE" != "1" ]; then
  install_skill "$HOME/.claude/skills" "Claude"
  INSTALLED="$INSTALLED claude"
fi
if [ "$SKIP_CODEX" != "1" ]; then
  install_skill "${CODEX_HOME:-$HOME/.codex}/skills" "Codex"
  install_skill "$HOME/.agents/skills" "agentes (pasta compartilhada)"
  INSTALLED="$INSTALLED codex"
fi

# 3. Ferramenta pronta
APP_DIR="$HOME/Sprint"
APP_FILE="$APP_DIR/Sprint.html"
mkdir -p "$APP_DIR"
cp "$SKILL_SRC/assets/sprint.html" "$APP_FILE"
ok "Ferramenta gerada em $APP_FILE"

if [ "$NO_OPEN" != "1" ]; then
  if command -v open >/dev/null 2>&1; then open "$APP_FILE" && ok "Aberta no navegador"
  elif command -v xdg-open >/dev/null 2>&1; then (xdg-open "$APP_FILE" >/dev/null 2>&1 &) && ok "Aberta no navegador"
  else warn "Não encontrei como abrir o navegador. Abra manualmente: $APP_FILE"
  fi
fi

# 4. Próximos passos
printf '\n  Pronto. Como usar:\n'
printf '    Navegador  %s  (modo local, já com um projeto de exemplo)\n' "$APP_FILE"
case "$INSTALLED" in *claude*) printf '    Claude     digite /sprint ou peça "abra a Sprint": vira um artefato compartilhado\n' ;; esac
case "$INSTALLED" in *codex*) printf '    Codex      digite $sprint ou peça "abra a Sprint"\n' ;; esac
printf '\n  Abra uma nova conversa para o agente reconhecer a skill.\n\n'
