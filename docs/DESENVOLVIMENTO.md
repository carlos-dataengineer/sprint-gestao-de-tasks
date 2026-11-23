# Desenvolvimento

## Requisitos

- Python 3.9+ (só para build e testes; a ferramenta e os instaladores não usam Python).
- Para o teste no navegador e as capturas: `pip install playwright && python -m playwright install chromium`.

## Ciclo

```bash
python scripts/build.py          # gera app/ e skills/sprint/assets/
python tests/validate_repo.py    # estrutura, versões, instaladores, links do README
python tests/test_smoke.py       # navegador: modo local e compartilhado simulado
python scripts/screenshots.py    # atualiza docs/images/
```

Para ver a página: abra `app/index.html` no navegador, ou sirva a pasta com `python -m http.server` e abra `http://localhost:8000/app/`.

## Testar o modo compartilhado sem o Claude

`tests/test_smoke.py` injeta um `window.claude` falso com banco em memória e três níveis de acesso (proprietário, contribuidor, visualizador). Use o mesmo trecho (`FAKE_CLAUDE`) no console do navegador antes de carregar a página para depurar.

## Testar os instaladores sem mexer na sua máquina

```bash
HOME=$(mktemp -d) bash install.sh --no-open
```

No Windows, rode o PowerShell com `USERPROFILE` apontando para uma pasta vazia.

## Publicar no Claude a partir do repositório

Peça ao Claude: "publique `skills/sprint/assets/sprint-artifact.html` como artefato com as capacidades de `skills/sprint/references/CAPACIDADES.md`".
