# Formato dos dados

## Coleções (modo compartilhado)

| Caminho | Conteúdo |
|---|---|
| `projeto/config` | `nome`, `descricao`, `inicio` (AAAA-MM-DD, segunda-feira da S1), `sprints` (1–52), `feriados` (extras, lista AAAA-MM-DD), `feriadosAuto` (bool), `feriadosFacultativos` (bool), `status` (`bom`/`riscos`/`problemas`), `statusModo` (`auto`/`manual`) |
| `fases/<id>` | Uma task por documento (campos abaixo) |
| `atencao/<id>` | `frente`, `texto`, `responsavel`, `prazo` (AAAA-MM-DD), `ordem` |

### Campos de uma task

| Campo | Valores |
|---|---|
| `nome` | texto (obrigatório) |
| `responsavel` | texto; várias pessoas separadas por `/` ou `,` (ex.: `Ana / Bruno`) |
| `prioridade` | `alta`, `media`, `baixa` |
| `inicio`, `fim` | AAAA-MM-DD. Obrigatórios fora do Backlog. A barra do cronograma termina no `fim`. |
| `coluna` | `backlog`, `afazer`, `andamento`, `bloqueado`, `validacao`, `concluido`, `historico` |
| `status` | `iniciar`, `andamento`, `concluido` (o painel calcula `atrasado` sozinho) |
| `descricao` | texto |
| `ordem` | número: ordem no cronograma |
| `ordemQuadro` | número: ordem dentro da coluna |
| `rotulo` | texto curto opcional na barra |
| `marco` | bool: mostra ◆ |
| `destaque` | bool: nome em negrito |
| `imagens` | lista `{id, nome, destaque}` (ids do `assets`) |
| `atualizadoEm`, `arquivadoEm` | ISO 8601 |

Coluna e status andam juntos: `backlog`/`afazer` → `iniciar`; `andamento`/`bloqueado`/`validacao` → `andamento`; `concluido`/`historico` → `concluido`.

## Gravar no artefato (ArtifactData)

Depois de publicar, use uma única operação `batch`, por exemplo:

```json
[
  { "op": "set", "collection": "projeto", "doc_id": "config",
    "data": { "nome": "Lançamento do app", "inicio": "2026-12-07", "sprints": 6, "feriadosAuto": true } },
  { "op": "set", "collection": "fases", "doc_id": "t1",
    "data": { "nome": "Protótipo das telas", "responsavel": "Ana", "prioridade": "alta",
              "inicio": "2026-12-07", "fim": "2026-12-11", "coluna": "afazer", "status": "iniciar",
              "ordem": 1, "ordemQuadro": 1 } }
]
```

Confira o formato exato das operações na definição da ferramenta `ArtifactData` desta sessão.

## Backup (JSON exportado pelo botão Dados)

```json
{
  "formato": "sprint-gestao-de-tasks",
  "versao": 2,
  "projeto": { "nome": "…", "inicio": "AAAA-MM-DD", "sprints": 8 },
  "fases":   [ { "id": "t1", "nome": "…", "coluna": "afazer", "inicio": "…", "fim": "…" } ],
  "atencao": [ { "id": "a1", "frente": "…", "texto": "…" } ],
  "imagens": { }
}
```

`formato` e a lista `fases` são obrigatórios para importar. Ids repetidos ou ausentes são gerados de novo; task fora do Backlog sem datas volta para o Backlog.

## Entregar já preenchido (modo local)

Faça uma cópia de `assets/sprint.html` e insira, logo antes da última `<script>` do arquivo, uma linha com o backup no formato acima:

```html
<script>window.SPRINT_SEED = {"formato":"sprint-gestao-de-tasks","versao":2,"projeto":{…},"fases":[…],"atencao":[]};</script>
```

O painel usa esse conteúdo na primeira abertura, quando o navegador ainda não tem dados da Sprint. Se já tiver, salve o JSON num arquivo e peça para a pessoa usar **Dados → Importar backup**.
