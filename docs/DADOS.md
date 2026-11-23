# Dados

O modelo completo (coleções, campos, regras entre coluna e status, formato do backup e `window.SPRINT_SEED`) está em [skills/sprint/references/FORMATO-DADOS.md](../skills/sprint/references/FORMATO-DADOS.md). As capacidades e permissões do artefato estão em [skills/sprint/references/CAPACIDADES.md](../skills/sprint/references/CAPACIDADES.md).

## Onde ficam os dados

| Modo | Onde | Quem vê | Backup |
|---|---|---|---|
| Local | `localStorage` do navegador (chave `sprint.v2`) | Só quem usa aquele navegador | Dados → Exportar backup (JSON) |
| Compartilhado | Banco do artefato no Claude | Todos com acesso ao artefato | Dados → Exportar backup (JSON) |

## Migração

- Dados da versão 1 (chave `sprint.demo.v1`) são lidos automaticamente na primeira abertura da 2.0.
- Para levar um painel local para o Claude, exporte o JSON e peça ao Claude: "publique a Sprint e importe este backup". A skill grava as tasks no banco do artefato.
