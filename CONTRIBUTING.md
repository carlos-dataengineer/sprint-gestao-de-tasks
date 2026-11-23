# Como contribuir

Obrigado por querer melhorar a Sprint.

## Antes de começar

1. Veja se já existe uma [issue](https://github.com/carlos-dataengineer/sprint-gestao-de-tasks/issues) sobre o assunto.
2. Para mudanças grandes, abra uma issue primeiro e conte o que pretende fazer.

## Como o projeto é organizado

| Caminho | O que é |
|---|---|
| `src/sprint.html` | **Fonte única** da ferramenta (HTML, CSS e JS, sem dependências). Edite aqui. |
| `scripts/build.py` | Gera `app/index.html` e `skills/sprint/assets/*` a partir da fonte. |
| `skills/sprint/` | A skill instalada no Claude e no Codex. |
| `install.*`, `uninstall.*` | Instaladores. Os `.ps1` precisam ser ASCII puro, sem BOM e com CRLF. |
| `tests/` | Validação estática e teste no navegador. |
| `docs/` | Arquitetura, dados, desenvolvimento e imagens do README. |

Detalhes em [docs/DESENVOLVIMENTO.md](docs/DESENVOLVIMENTO.md).

## Passo a passo

```bash
git clone https://github.com/carlos-dataengineer/sprint-gestao-de-tasks.git
cd sprint-gestao-de-tasks
# edite src/sprint.html
python scripts/build.py
python tests/validate_repo.py
pip install playwright && python -m playwright install chromium
python tests/test_smoke.py
```

## Regras

- Não edite os arquivos gerados à mão: o CI recusa se estiverem diferentes do build.
- Preserve os dois modos de dados e os nomes de coleções e campos: artefatos já publicados dependem deles.
- Não adicione dependências externas nem serviços remotos sem discutir antes.
- Exemplos e capturas só com dados fictícios.
- Registre a mudança em `CHANGELOG.md`, na seção da próxima versão.
- Mensagens de commit no estilo [Conventional Commits](https://www.conventionalcommits.org/pt-br/) (`feat:`, `fix:`, `docs:`…).

## Nova versão (mantenedor)

1. Atualize `VERSION`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `CITATION.cff` e `CHANGELOG.md`.
2. `python scripts/build.py` e os testes.
3. Crie a tag `vX.Y.Z` e envie: o workflow de release publica os pacotes.
