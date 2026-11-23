---
name: sprint
description: Abre a Sprint — Gestão de Tasks, um painel pronto que junta cronograma de sprints (gantt semanal), quadro Kanban, overview de métricas, nota de saúde do projeto e pontos de atenção. Use quando a pessoa pedir "sprint", "/sprint", "$sprint", "abrir a Sprint", um painel de tasks, um quadro Kanban, um cronograma ou gantt de sprints, acompanhar entregas e prazos do time, ou quando ela listar tarefas e pedir para organizar num quadro. Use também para pedir mudanças na própria ferramenta.
license: MIT
---

# Sprint — Gestão de Tasks

A Sprint é uma ferramenta pronta, em um único arquivo HTML. **Nunca reescreva a ferramenta de memória e nunca gere uma versão "parecida"**: use sempre os arquivos de `assets/`, ao lado deste `SKILL.md`.

| Arquivo | Para quê |
|---|---|
| `assets/sprint-artifact.html` | Publicar como artefato no Claude (ferramenta Artifact). Fragmento sem `<html>`/`<body>`, como o artefato exige. Usa o banco compartilhado do artefato. |
| `assets/sprint.html` | Documento completo. Abre no navegador (Codex, terminal) e guarda os dados no navegador. |
| `references/CAPACIDADES.md` | Capacidades e regras de acesso do artefato no Claude. |
| `references/FORMATO-DADOS.md` | Coleções, campos, formato de backup e como entregar o painel já preenchido. |
| `references/EVOLUIR.md` | Como alterar a ferramenta quando a pessoa pedir uma melhoria. |

A página detecta sozinha onde está:

- **Modo compartilhado** (etiqueta *Compartilhado*): aberta como artefato do Claude com as capacidades `db`, `user` e `assets`. Todos com acesso veem as mesmas tasks em tempo real e as permissões seguem o compartilhamento.
- **Modo local** (etiqueta *Local*): aberta como arquivo. Começa com um projeto fictício de exemplo e salva no `localStorage` do navegador.

## 1. Escolha como entregar

Siga a primeira opção que o ambiente permitir.

**A. Claude com a ferramenta Artifact** (app desktop do Claude, Claude Code com artefatos)

1. Liste os artefatos da pessoa (`action: "list"`). Se já existir um chamado **Sprint** (ou com o nome do projeto dela), ofereça abrir esse (`action: "open"`) em vez de criar outro: cada artefato tem o próprio banco.
2. Para criar, publique `assets/sprint-artifact.html` **sem alterar o código**, com:
   - `icon: "calendar"` e `description: "Cronograma de sprints, quadro Kanban e saúde do projeto"`;
   - `capabilities` exatamente como em `references/CAPACIDADES.md`.
   Se a ferramenta pedir um passo de design, o arquivo já está pronto: não mude o visual.
3. O banco começa vazio. Se a pessoa já contou o projeto ou as tasks, ou trouxe um backup JSON exportado pela Sprint (campo `formato: "sprint-gestao-de-tasks"`), grave-os depois de publicar (ferramenta `ArtifactData`, operação `batch`) seguindo `references/FORMATO-DADOS.md`. Se não contou, diga que ela começa em **Editar projeto** e **+ Nova Task**.
4. Faça uma leitura (`list`) de `fases` para conferir o que gravou e entregue o link.

**B. claude.ai sem a ferramenta Artifact** (chat com artefatos HTML)

Crie um artefato HTML cujo conteúdo é **exatamente** `assets/sprint.html`, sem resumir nem cortar. Avise que nesse formato os dados ficam só naquela visualização e que o botão **Dados → Exportar** guarda uma cópia.

**C. Codex, Claude Code no terminal ou qualquer agente sem artefatos**

1. Copie `assets/sprint.html` para `~/Sprint/Sprint.html` (crie a pasta se faltar). Se já existir um arquivo diferente ali, pergunte antes de sobrescrever. Os dados ficam no navegador, não no arquivo, então substituir o arquivo não apaga as tasks.
2. Se a pessoa contou o projeto ou as tasks, entregue o painel preenchido como descrito em `references/FORMATO-DADOS.md` (seção "Entregar já preenchido").
3. Abra no navegador padrão:
   - Windows: `Start-Process "$HOME\Sprint\Sprint.html"`
   - macOS: `open ~/Sprint/Sprint.html`
   - Linux: `xdg-open ~/Sprint/Sprint.html`
4. Diga o caminho do arquivo.

## 2. Depois de entregar

Explique em poucas linhas:

- **Cronograma**: barras por status (concluído, em andamento, atrasado, a iniciar), marcos ◆, linha de Hoje e feriados nacionais do Brasil automáticos.
- **Quadro**: Backlog → A fazer → Em andamento → Bloqueado → Em validação → Concluído → Histórico. Arrastar um card muda a etapa e o cronograma acompanha.
- **Status Geral**: nota de saúde 0–100 (Ritmo 35%, Prazos 25%, Bloqueios 15%, Previsão 25%).
- **Atalhos**: `N` nova task, `P` ponto de atenção, `/` buscar, `F` período completo, `E` editar projeto, `D` dados, `T` tema, `H` histórico, `1`–`7` colunas, `?` ajuda.
- **Dados**: no modo local, exportar backup (JSON), planilha (CSV), importar, restaurar o exemplo ou começar do zero. No modo compartilhado, exportar JSON e CSV.

## 3. Pedidos de mudança na ferramenta

Quando a pessoa pedir uma melhoria ("adicione um filtro por prioridade", "mude as cores"), siga `references/EVOLUIR.md`. Resumo: altere os dois arquivos de `assets/` do mesmo jeito, teste, e entregue de novo pela opção do passo 1. Se a pasta da skill não puder ser gravada, entregue o arquivo novo e avise que a melhoria não fica para as próximas instalações.

## Regras

- Não invente recursos: não há login próprio, notificações, integração com Jira/Azure ou sincronização entre navegadores no modo local.
- Não grave senhas, chaves ou dados sensíveis em tasks: todos com acesso ao painel leem.
- Dados de exemplo são fictícios. Não use nomes reais de clientes ou pessoas sem a pessoa pedir.
