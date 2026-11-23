# Evoluir a ferramenta

Trate o pedido como uma mudança de produto.

1. Leia o trecho atual em `assets/sprint.html` antes de mexer. O código é HTML, CSS e JavaScript puros, sem build.
2. Aplique a mesma alteração em `assets/sprint.html` e em `assets/sprint-artifact.html`. O segundo é o mesmo conteúdo sem `<!doctype>`, `<html>`, `<head>` e `<body>`.
3. Preserve: os dois modos de dados (`startClaude` e `startLocal`), os nomes de coleções e campos (o banco de artefatos já publicados depende deles), o escape de textos (`esc`) e as regras de permissão (`setEdit`).
4. Teste abrindo o arquivo no navegador: console sem erros, criar, mover e excluir uma task, recarregar e ver os dados.
5. Entregue pela mesma opção usada antes (artefato ou arquivo). Para artefato existente, republique no mesmo link e omita `capabilities` para manter as que já estão lá.
6. Diga o que mudou.

Se a pasta da skill não puder ser gravada, entregue o arquivo novo e avise que a melhoria não fica nas próximas instalações.

Quem quiser contribuir com a mudança para todo mundo: o código-fonte fica em `src/sprint.html` no repositório e `python scripts/build.py` gera os arquivos de `assets/`.
