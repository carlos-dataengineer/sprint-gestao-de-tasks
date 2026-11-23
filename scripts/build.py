#!/usr/bin/env python3
"""Gera os arquivos distribuídos da Sprint a partir de src/sprint.html.

Saídas:
  app/index.html                            documento completo (demo e GitHub Pages)
  skills/sprint/assets/sprint.html          documento completo usado pela skill (modo local)
  skills/sprint/assets/sprint-artifact.html fragmento para publicar como artefato no Claude

Uso:
  python scripts/build.py          gera os arquivos
  python scripts/build.py --check  falha se os arquivos gerados estiverem desatualizados
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "sprint.html"
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

OUT_APP = ROOT / "app" / "index.html"
OUT_SKILL = ROOT / "skills" / "sprint" / "assets" / "sprint.html"
OUT_ARTIFACT = ROOT / "skills" / "sprint" / "assets" / "sprint-artifact.html"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def build() -> dict[Path, str]:
    src = read(SRC).strip() + "\n"
    stamp = f"<!-- Sprint — Gestão de Tasks v{VERSION} · https://github.com/carlos-dataengineer/sprint-gestao-de-tasks · MIT -->\n"
    first, rest = src.split("\n", 1)
    fragment = first + "\n" + stamp + rest
    head_end = src.index("</style>\n") + len("</style>\n")
    full = (
        "<!doctype html>\n<html lang=\"pt-BR\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
        f"<meta name=\"generator\" content=\"Sprint {VERSION}\">\n"
        + stamp
        + src[:head_end]
        + "</head>\n<body>\n"
        + src[head_end:].rstrip()
        + "\n</body>\n</html>\n"
    )
    return {OUT_APP: full, OUT_SKILL: full, OUT_ARTIFACT: fragment}


def main() -> int:
    check = "--check" in sys.argv
    stale = []
    for path, content in build().items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == content:
            continue
        if check:
            stale.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
            print(f"gerado: {path.relative_to(ROOT).as_posix()}")
    if stale:
        print("Arquivos desatualizados. Rode: python scripts/build.py")
        for s in stale:
            print(f"  - {s}")
        return 1
    if check:
        print("Arquivos gerados em dia.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
