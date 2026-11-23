#!/usr/bin/env python3
"""Gera as capturas de tela do README em docs/images/.

Usa o projeto fictício de exemplo da própria ferramenta (datas relativas a hoje).

Requer: pip install playwright && python -m playwright install chromium
Uso:    python scripts/screenshots.py
"""
from __future__ import annotations

from pathlib import Path

from playwright.sync_api import Page, sync_playwright

ROOT = Path(__file__).resolve().parent.parent
APP = (ROOT / "app" / "index.html").as_uri()
OUT = ROOT / "docs" / "images"


def open_app(page: Page) -> None:
    page.goto(APP)
    page.wait_for_selector(".card", state="attached")
    page.wait_for_function("document.fonts && document.fonts.status === 'loaded'")
    page.wait_for_timeout(700)


def save(target, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    target.screenshot(path=str(OUT / name))
    print("ok", name)


def section(page: Page, heading_id: str):
    return page.locator(f"section:has(#{heading_id})")


def main() -> None:
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception:
            browser = p.chromium.launch(channel="msedge")

        def ctx(w=1440, h=900, mobile=False):
            return browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=3 if mobile else 2,
                                       is_mobile=mobile, has_touch=mobile, locale="pt-BR")

        c = ctx(); pg = c.new_page(); open_app(pg)
        save(pg, "visao-geral.png")
        save(pg.locator(".summary"), "overview-status.png")
        save(section(pg, "h-crono"), "cronograma.png")
        save(section(pg, "h-att"), "pontos-atencao.png")
        save(section(pg, "h-kb"), "quadro.png")

        pg.click("#hs-help"); pg.wait_for_timeout(150)
        save(pg.locator(".summary .panel").nth(1), "saude-calculo.png")
        pg.click("#hs-help")

        pg.locator(".card", has_text="Implementar validações").click(); pg.wait_for_timeout(200)
        save(pg, "editar-task.png"); pg.keyboard.press("Escape")

        pg.keyboard.press("?"); pg.wait_for_timeout(150)
        save(pg.locator(".modal"), "atalhos.png"); pg.keyboard.press("Escape")

        pg.keyboard.press("d"); pg.wait_for_timeout(150)
        save(pg.locator(".modal"), "dados.png"); pg.keyboard.press("Escape")

        pg.keyboard.press("e"); pg.wait_for_timeout(150)
        save(pg.locator(".modal"), "editar-projeto.png"); pg.keyboard.press("Escape")

        pg.keyboard.press("h"); pg.wait_for_timeout(150)
        pg.locator('.col[data-col="historico"]').scroll_into_view_if_needed()
        save(section(pg, "h-kb"), "historico.png"); pg.keyboard.press("h")

        pg.evaluate("window.scrollTo(0,0)")
        pg.keyboard.press("t"); pg.wait_for_timeout(250)
        save(pg, "tema-claro.png")
        c.close()

        c = ctx(390, 844, mobile=True); pg = c.new_page(); open_app(pg); save(pg, "celular.png")
        pg.locator("#h-kb").scroll_into_view_if_needed(); pg.wait_for_timeout(200); save(pg, "celular-quadro.png"); c.close()
        browser.close()


if __name__ == "__main__":
    main()
