#!/usr/bin/env bash
# Remove a skill da Sprint do Claude e do Codex.
#
#   curl -fsSL https://raw.githubusercontent.com/carlos-dataengineer/sprint-gestao-de-tasks/main/uninstall.sh | bash
#
# Apaga apenas pastas cujo SKILL.md se chama "sprint" (ou o nome antigo "sprint-task-management").
# A ferramenta em ~/Sprint fica, a menos que você use --all (ou SPRINT_UNINSTALL_ALL=1).
# As tasks salvas no navegador e os artefatos publicados no Claude não são tocados.
set -euo pipefail

ALL="${SPRINT_UNINSTALL_ALL:-0}"
[ "${1:-}" = "--all" ] && ALL=1

for dir in "$HOME/.claude/skills" "${CODEX_HOME:-$HOME/.codex}/skills" "$HOME/.agents/skills"; do
  for name in sprint sprint-task-management; do
    t="$dir/$name"
    if [ -f "$t/SKILL.md" ] && grep -Eq "^name:[[:space:]]*$name[[:space:]]*$" "$t/SKILL.md"; then
      rm -rf "$t"
      echo "  removido: $t"
    fi
  done
done

APP="$HOME/Sprint/Sprint.html"
if [ "$ALL" = "1" ] && [ -f "$APP" ]; then
  rm -f "$APP"
  rmdir "$HOME/Sprint" 2>/dev/null || true
  echo "  removido: $APP"
elif [ -f "$APP" ]; then
  echo "  mantido: $APP (use --all para remover)"
fi
echo "  Sprint desinstalada."
