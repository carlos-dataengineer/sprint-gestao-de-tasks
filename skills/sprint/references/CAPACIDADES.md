# Capacidades do artefato no Claude

Ao publicar `assets/sprint-artifact.html` com a ferramenta Artifact, passe exatamente:

```json
{
  "db": {
    "rules": [
      { "path": "",        "read": "view", "write": "admin" },
      { "path": "fases",   "read": "view", "write": "interact" },
      { "path": "atencao", "read": "view", "write": "interact" }
    ]
  },
  "user": {},
  "assets": { "upload": "interact" },
  "downloads": true
}
```

| Capacidade | Uso na Sprint |
|---|---|
| `db` | Banco compartilhado: `projeto/config`, `fases` (tasks) e `atencao` (pontos de atenção). |
| `user` | Descobre o nível de quem está vendo para liberar ou esconder botões. |
| `assets` | Imagens anexadas às tasks. |
| `downloads` | Exportar backup JSON e planilha CSV. |

## Quem pode o quê

| Nível no compartilhamento | O que faz |
|---|---|
| Proprietário e Editores | Tudo, inclusive a estrutura: nome, início da S1, nº de sprints, feriados e status fixado. |
| Contribuidores | Criam, editam, movem e arquivam tasks e pontos de atenção; anexam imagens. |
| Comentaristas e Visualizadores | Só leem. |

O nível Editor também permite publicar novas versões da página. Para quem só usa as tasks, prefira Contribuidor.

## Se a página não conseguir o banco

Sem `db` (capacidade não declarada, pessoa deslogada ou visualização sem runtime), a página cai para o modo local e mostra um aviso. Republique com as capacidades acima.
