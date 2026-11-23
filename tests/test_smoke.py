#!/usr/bin/env python3
"""Teste de fumaça da Sprint no navegador (Playwright).

Cobre o modo local (arquivo aberto no navegador) e o modo compartilhado
(artefato do Claude), este com um `window.claude` simulado em memória.

Requer: pip install playwright && python -m playwright install chromium
Uso:    python tests/test_smoke.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
APP = (ROOT / "skills" / "sprint" / "assets" / "sprint.html").as_uri()

# window.claude falso: db em memória com onSnapshot, user sem edição completa.
FAKE_CLAUDE = """
(() => {
  const data = { "projeto/config": null, fases: {}, atencao: {} };
  const subs = {};
  const snapCol = n => ({ docs: Object.entries(data[n]).map(([id, v]) => ({ id, data: () => JSON.parse(JSON.stringify(v)) })) });
  const snapDoc = p => ({ exists: !!data[p], data: () => JSON.parse(JSON.stringify(data[p] || {})) });
  const fire = k => (subs[k] || []).forEach(fn => fn(k.includes("/") ? snapDoc(k) : snapCol(k)));
  let n = 0;
  const db = {
    doc(path) {
      return {
        onSnapshot(fn) { (subs[path] = subs[path] || []).push(fn); setTimeout(() => fn(snapDoc(path))); return () => {}; },
        async set(v) { if (path === "projeto/config") { data[path] = v; fire(path); return; } const [c, id] = path.split("/"); data[c][id] = v; fire(c); },
        async update(v) { if (path === "projeto/config") { data[path] = Object.assign({}, data[path], v); fire(path); return; } const [c, id] = path.split("/"); Object.assign(data[c][id], v); fire(c); },
        async delete() { const [c, id] = path.split("/"); delete data[c][id]; fire(c); },
      };
    },
    collection(name) {
      return {
        onSnapshot(fn) { (subs[name] = subs[name] || []).push(fn); setTimeout(() => fn(snapCol(name))); return () => {}; },
        async add(v) { const id = "x" + (++n); data[name][id] = v; fire(name); return { id }; },
      };
    },
  };
  const level = window.__SPRINT_LEVEL__ || "contributor";
  const user = {
    async isOwner() { return level === "owner"; },
    async canEdit() { return level === "owner"; },
    async can() { return level !== "viewer"; },
  };
  window.__fakeDb = data;
  window.claude = { use: async name => ({ db, user })[name] || null };
})();
"""

failures: list[str] = []


def check(cond: bool, msg: str) -> None:
    print(("ok   " if cond else "FALHA ") + msg)
    if not cond:
        failures.append(msg)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception:
            browser = p.chromium.launch(channel="msedge")

        # ---------- modo local ----------
        ctx = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True, locale="pt-BR")
        page = ctx.new_page()
        errors: list[str] = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: m.type == "error" and errors.append(m.text))
        page.goto(APP)
        page.wait_for_selector(".card", state="attached")
        check(page.locator("#mode-tag").text_content().strip() == "Local", "modo local identificado")
        check(page.locator(".card").count() >= 8, "exemplo fictício carregado no quadro")
        check(page.locator(".g-row").count() >= 5, "cronograma desenhado")
        check("Squad Atlas" in page.title(), "título usa o nome do projeto")

        page.keyboard.press("?")
        check(page.locator(".kbd-list").is_visible(), "atalho ? abre a ajuda")
        page.keyboard.press("Escape")
        check(page.locator("#modal-root").inner_html() == "", "Esc fecha a janela")

        page.keyboard.press("n")
        page.fill("#m-nome", "Task criada pelo teste")
        page.fill("#m-responsavel", "Pessoa Teste")
        page.click("#m-save")
        page.wait_for_timeout(200)
        check(page.locator(".card", has_text="Task criada pelo teste").count() == 1, "atalho N cria task")
        page.reload()
        page.wait_for_selector(".card", state="attached")
        check(page.locator(".card", has_text="Task criada pelo teste").count() == 1, "task persiste após recarregar (localStorage)")

        page.keyboard.press("/")
        check(page.evaluate("document.activeElement.id") == "f-q", "atalho / foca a busca")
        page.keyboard.type("Task criada")
        page.wait_for_timeout(100)
        visible = page.locator(".col:not([data-col=historico]) .card").count()
        check(visible == 1, f"busca filtra o quadro ({visible} card)")
        page.keyboard.press("Escape")

        page.keyboard.press("d")
        with page.expect_download() as dl:
            page.click("#d-json")
        path = dl.value.path()
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        check(data.get("formato") == "sprint-gestao-de-tasks" and len(data["fases"]) >= 11, "exportar backup JSON")
        with page.expect_download() as dl2:
            page.click("#d-csv")
        csv = Path(dl2.value.path()).read_text(encoding="utf-8-sig")
        check(csv.startswith("Task;Responsável"), "exportar planilha CSV")
        page.click("#d-zero")
        page.click("#m-yes")
        page.wait_for_timeout(150)
        check(page.locator(".card").count() == 0, "começar do zero limpa o quadro")
        page.keyboard.press("d")
        page.set_input_files("#d-file", path)
        page.click("#m-yes")
        page.wait_for_timeout(200)
        check(page.locator(".card", has_text="Task criada pelo teste").count() == 1, "importar backup restaura as tasks")

        check(not errors, "sem erros no console (modo local)" + (": " + "; ".join(errors) if errors else ""))
        ctx.close()

        # ---------- painel entregue já preenchido (window.SPRINT_SEED) ----------
        ctx = browser.new_context(viewport={"width": 1280, "height": 860}, locale="pt-BR")
        seed = {"formato": "sprint-gestao-de-tasks", "versao": 2, "projeto": {"nome": "Projeto Semente", "inicio": "2026-01-05", "sprints": 4},
                "fases": [{"nome": "Task da semente", "responsavel": "Ana", "inicio": "2026-01-05", "fim": "2026-01-09", "coluna": "andamento"},
                          {"nome": "Sem datas fora do backlog", "coluna": "afazer"}],
                "atencao": [{"frente": "Geral", "texto": "Ponto da semente"}]}
        ctx.add_init_script("window.SPRINT_SEED = " + json.dumps(seed) + ";")
        page = ctx.new_page()
        page.goto(APP)
        page.wait_for_selector(".card", state="attached")
        check("Projeto Semente" in page.title(), "SPRINT_SEED define o projeto")
        check(page.locator(".card", has_text="Task da semente").count() == 1, "SPRINT_SEED cria as tasks")
        check(page.locator('.col[data-col="backlog"] .card', has_text="Sem datas").count() == 1, "task sem datas vai para o Backlog")
        ctx.close()

        # ---------- modo compartilhado (Claude simulado) ----------
        for level, can_edit, can_admin in [("owner", True, True), ("contributor", True, False), ("viewer", False, False)]:
            ctx = browser.new_context(viewport={"width": 1280, "height": 860}, locale="pt-BR")
            ctx.add_init_script(f"window.__SPRINT_LEVEL__ = {json.dumps(level)};" + FAKE_CLAUDE)
            page = ctx.new_page()
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto(APP)
            page.wait_for_function("document.getElementById('mode-tag').textContent === 'Compartilhado'")
            page.wait_for_timeout(200)
            check(page.locator(".card").count() == 0, f"[{level}] banco vazio não recebe dados de exemplo")
            check(page.locator("#btn-card").is_visible() == can_edit, f"[{level}] botão Nova Task conforme permissão")
            check(page.locator("#btn-config").is_visible() == can_admin, f"[{level}] Editar projeto só para edição completa")
            if can_edit:
                page.click("#btn-card")
                page.fill("#m-nome", "Task compartilhada")
                page.click("#m-save")
                page.wait_for_timeout(200)
                stored = page.evaluate("Object.values(window.__fakeDb.fases).map(f => f.nome)")
                check(stored == ["Task compartilhada"], f"[{level}] task gravada no banco do artefato")
            check(not errors, f"[{level}] sem erros de página" + (": " + "; ".join(errors) if errors else ""))
            ctx.close()

        browser.close()

    print()
    if failures:
        print(f"{len(failures)} falha(s).")
        return 1
    print("Teste de fumaça passou.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
