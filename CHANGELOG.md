# Histórico de versões

O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e as versões seguem o [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [2.0.0] - 2026-11-23

### Adicionado
- Instalação com um comando (`install.ps1` para Windows, `install.sh` para macOS e Linux) que instala a skill no Claude e no Codex e já gera a ferramenta em `~/Sprint/Sprint.html`, aberta no navegador.
- Desinstaladores (`uninstall.ps1` e `uninstall.sh`).
- Plugin do Claude Code (`.claude-plugin/`), instalável por `/plugin marketplace add`.
- Dois modos na mesma página: **compartilhado** (artefato do Claude com banco em tempo real e permissões do compartilhamento) e **local** (navegador, com `localStorage`).
- Atalhos de teclado (`N`, `P`, `/`, `F`, `E`, `D`, `T`, `H`, `1`–`7`, `?`, `Esc`) e janela de ajuda.
- Botão **Dados**: exportar backup JSON e planilha CSV; no modo local, importar backup, restaurar o exemplo e começar do zero.
- `window.SPRINT_SEED` para a skill entregar o painel já preenchido.
- Projeto de exemplo com datas relativas a hoje, para nunca parecer desatualizado.
- Configuração do Codex em `skills/sprint/agents/openai.yaml`.
- Teste de fumaça no navegador (Playwright), validação estática do repositório, CI em Linux, macOS e Windows, e release automática por tag.
- README com capturas de tela, casos de uso, atalhos e perguntas frequentes.

### Alterado
- A skill passa a se chamar `sprint` (antes `sprint-task-management`); o instalador remove a versão antiga.
- Estrutura do repositório: fonte única em `src/sprint.html`, arquivos gerados por `scripts/build.py`.
- O título da página mostra o nome do projeto.

### Removido
- Scripts Python de instalação (`sprint-skill/scripts/*.py`): a instalação não depende mais de Python.

## [1.2.0] - 2026-11-21

- Bootstrap de instalação que cria `Sprint.html`.

## [1.1.0] - 2026-11-21

- Apresentação do projeto reescrita com diagramas.

## [1.0.0] - 2026-11-19

- Primeira versão pública: aplicação HTML independente, armazenamento local, dados fictícios e Agent Skill.
