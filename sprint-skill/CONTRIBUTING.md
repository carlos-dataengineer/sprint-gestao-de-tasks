# Como contribuir

Obrigado por querer ajudar a melhorar a Sprint.

## Antes de começar

1. Leia o README e os documentos em `docs/`.
2. Confira se já existe uma issue sobre a ideia ou o problema.
3. Explique o que pretende mudar e por que isso ajuda quem usa a ferramenta.

## Desenvolvimento

- Mantenha a aplicação independente e compatível com navegadores modernos.
- Preserve os recursos existentes que não fazem parte da mudança.
- Não inclua dados reais de clientes, projetos, pessoas ou empresas nos exemplos.
- Não adicione dependências, serviços remotos ou coleta de dados sem explicar e documentar a necessidade.
- Atualize a documentação quando alterar funcionalidades ou regras.

## Testes

Execute:

```bash
python -m unittest discover -s sprint-skill/tests -v
python sprint-skill/scripts/install.py --output /tmp/Sprint.html
```

Confira se o artefato foi criado e se as mudanças solicitadas aparecem nele.

## Pull requests

Descreva o problema, a solução adotada, os arquivos alterados e os testes executados. Inclua imagens ou exemplos quando ajudarem a entender uma mudança visual.
