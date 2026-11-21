# Como os dados da Sprint são organizados

A aplicação guarda os dados no próprio navegador, usando `localStorage`. Não existe banco de dados remoto nem sincronização entre pessoas nesta versão.

## Grupos de dados

| Grupo | O que guarda |
|---|---|
| `cfg` | Configurações do projeto, calendário e quantidade de sprints |
| `fases` | Tarefas, responsáveis, datas, prioridades, status e anexos |
| `att` | Pontos de atenção, riscos e dependências |
| `assets` | Imagens anexadas, armazenadas localmente |

## Persistência

- A chave usada pela versão atual é `sprint.demo.v1`.
- Na primeira abertura, sem dados salvos, a aplicação carrega o conjunto fictício `DEMO`.
- Alterações feitas pela pessoa usuária são salvas no navegador e perfil atuais.
- Imagens anexadas são convertidas em Data URL e armazenadas localmente.

## Limites

O armazenamento local não compartilha dados entre dispositivos, navegadores ou usuários. Apagar os dados do navegador pode remover as informações salvas. Não use o `localStorage` para guardar senhas, tokens ou informações confidenciais.

## Possíveis evoluções

Uma futura versão multiusuário poderá exigir API, backend, banco de dados, autenticação, controle de permissões, armazenamento de anexos, sincronização e rotinas de backup. Esses recursos não fazem parte da versão atual.
