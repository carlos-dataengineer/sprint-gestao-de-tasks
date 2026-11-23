# Política de segurança

## Versões com suporte

| Versão | Suporte |
|---|---|
| 2.x | ✅ |
| 1.x | ❌ (atualize rodando o instalador de novo) |

## Como a Sprint trata os dados

- **Modo local** (arquivo no navegador): tudo fica no `localStorage` do navegador. Nada é enviado para servidores. Limpar os dados do navegador apaga o painel.
- **Modo compartilhado** (artefato do Claude): os dados ficam no banco do artefato, com o acesso definido pelo compartilhamento do Claude (Proprietário, Editor, Contribuidor, Visualizador). A Sprint não tem login próprio.
- A página carrega apenas as fontes Hanken Grotesk e Inter do Google Fonts. Sem internet, usa as fontes do sistema.
- Todo texto digitado é escapado antes de entrar na página, e imagens só são exibidas como `<img>`.

Não guarde senhas, tokens, chaves de API ou dados pessoais sensíveis nas tasks: qualquer pessoa com acesso ao painel consegue ler.

## Os instaladores

`install.ps1` e `install.sh` só gravam em `~/.claude/skills/sprint`, `~/.codex/skills/sprint` (ou `$CODEX_HOME`), `~/.agents/skills/sprint` e `~/Sprint/`. Eles não pedem administrador, não alteram configurações e não sobrescrevem uma pasta `sprint` que não seja desta skill. Leia o script antes de rodar, se preferir:

```bash
curl -fsSL https://raw.githubusercontent.com/carlos-dataengineer/sprint-gestao-de-tasks/main/install.sh | less
```

## Como relatar uma vulnerabilidade

Não abra issue pública. Use o [relato privado de vulnerabilidade](https://github.com/carlos-dataengineer/sprint-gestao-de-tasks/security/advisories/new) com os passos para reproduzir, o impacto e a versão. A resposta inicial sai em até 7 dias.
