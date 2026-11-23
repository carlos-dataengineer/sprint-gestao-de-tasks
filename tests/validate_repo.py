#!/usr/bin/env python3
"""Validações estáticas do repositório (sem navegador).

Confere: manifesto da skill, manifestos do plugin e do Codex, versão consistente,
arquivos gerados em dia, instaladores (ASCII sem BOM no PowerShell, LF no bash),
links e imagens do README, e termos proibidos (variável SPRINT_PROIBIDOS,
separados por vírgula) para evitar publicar dados privados.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []


def check(cond: bool, msg: str) -> None:
    if not cond:
        errors.append(msg)


def text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


# Skill
skill = text("skills/sprint/SKILL.md")
m = re.match(r"^---\n(.*?)\n---\n", skill, re.S)
check(bool(m), "SKILL.md sem frontmatter YAML")
if m:
    front = dict(re.findall(r"^(\w+):\s*(.+)$", m.group(1), re.M))
    check(front.get("name") == "sprint", "SKILL.md: name deve ser 'sprint'")
    desc = front.get("description", "")
    check(20 <= len(desc) <= 1024, "SKILL.md: description deve ter entre 20 e 1024 caracteres")
for ref in set(re.findall(r"`((?:assets|references|agents)/[^`]+)`", skill)):
    check((ROOT / "skills/sprint" / ref).exists(), f"SKILL.md cita {ref}, que não existe")
codex = text("skills/sprint/agents/openai.yaml")
check("display_name:" in codex and "$sprint" in codex, "agents/openai.yaml incompleto")

# Plugin e versão
version = text("VERSION").strip()
check(bool(re.fullmatch(r"\d+\.\d+\.\d+", version)), "VERSION fora do formato X.Y.Z")
plugin = json.loads(text(".claude-plugin/plugin.json"))
market = json.loads(text(".claude-plugin/marketplace.json"))
check(plugin.get("name") == "sprint", "plugin.json: name deve ser 'sprint'")
check(plugin.get("version") == version, f"plugin.json: versão {plugin.get('version')} difere de VERSION {version}")
entries = [p for p in market.get("plugins", []) if p.get("name") == "sprint"]
check(len(entries) == 1, "marketplace.json: precisa de uma entrada 'sprint'")
if entries:
    check(entries[0].get("version") == version, "marketplace.json: versão difere de VERSION")
check(f"## [{version}]" in text("CHANGELOG.md"), f"CHANGELOG.md sem a versão {version}")
check(f"version: {version}" in text("CITATION.cff"), "CITATION.cff com versão diferente de VERSION")

# Arquivos gerados
r = subprocess.run([sys.executable, str(ROOT / "scripts/build.py"), "--check"], capture_output=True, text=True)
check(r.returncode == 0, "arquivos gerados desatualizados (rode python scripts/build.py)")
for rel in ["app/index.html", "skills/sprint/assets/sprint.html", "skills/sprint/assets/sprint-artifact.html"]:
    p = ROOT / rel
    check(p.exists(), f"{rel} não existe")
    if p.exists():
        html = p.read_text(encoding="utf-8")
        check("<title>Sprint — Gestão de Tasks</title>" in html, f"{rel} sem o título")
        check("startClaude" in html and "startLocal" in html, f"{rel} sem os dois modos de dados")
        check(f"v{version}" in html, f"{rel} sem o carimbo da versão {version}")
artifact = text("skills/sprint/assets/sprint-artifact.html")
check(not re.search(r"<!doctype|<html|<body", artifact, re.I), "sprint-artifact.html não pode ter doctype/html/body")
check(text("skills/sprint/assets/sprint.html").lower().startswith("<!doctype html>"), "sprint.html precisa ser documento completo")

# Capacidades documentadas batem com o que a página pede
caps = text("skills/sprint/references/CAPACIDADES.md")
for name in ["db", "user", "assets", "downloads"]:
    check(f'"{name}"' in caps, f"CAPACIDADES.md sem a capacidade {name}")
    check(f'C.use("{name}")' in artifact, f"a página não usa a capacidade {name}")

# Instaladores
for rel in ["install.ps1", "uninstall.ps1"]:
    raw = (ROOT / rel).read_bytes()
    check(not raw.startswith(b"\xef\xbb\xbf"), f"{rel} não pode ter BOM (quebra o irm | iex)")
    check(all(b < 128 for b in raw), f"{rel} precisa ser ASCII puro (Windows PowerShell 5.1)")
for rel in ["install.sh", "uninstall.sh"]:
    raw = (ROOT / rel).read_bytes()
    check(raw.startswith(b"#!/usr/bin/env bash"), f"{rel} sem shebang")
    check(b"\r\n" not in raw, f"{rel} precisa de quebras de linha LF")
for rel in ["install.ps1", "install.sh"]:
    body = text(rel)
    check("carlos-dataengineer/sprint-gestao-de-tasks" in body, f"{rel} aponta para outro repositório")
    check("skills/sprint/SKILL.md" in body, f"{rel} não confere o pacote baixado")

# README
readme = text("README.md")
for img in re.findall(r'src="(docs/images/[^"]+)"', readme) + re.findall(r"\]\((docs/images/[^)]+)\)", readme):
    check((ROOT / img).exists(), f"README cita {img}, que não existe")
for link in re.findall(r"\]\(((?!https?://|#|mailto:)[^)\s]+)\)", readme):
    check((ROOT / link.split("#")[0]).exists(), f"README aponta para {link}, que não existe")
for must in ["install.ps1", "install.sh", "/sprint", "$sprint", "Atalhos"]:
    check(must in readme, f"README não menciona {must}")

# Termos proibidos (dados privados) em arquivos versionados
banned = [t.strip().lower() for t in os.environ.get("SPRINT_PROIBIDOS", "").split(",") if t.strip()]
if banned:
    files = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"], cwd=ROOT, capture_output=True, text=True).stdout.split("\n")
    for rel in filter(None, files):
        p = ROOT / rel
        if not p.is_file() or p.suffix.lower() in {".png", ".jpg", ".gif", ".webp"}:
            continue
        low = p.read_text(encoding="utf-8", errors="ignore").lower()
        for term in banned:
            if term in low:
                errors.append(f"termo proibido em {rel}")

if errors:
    print("Falhas:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print("Repositório válido.")
