# Como a Sprint é organizada

## Visão geral

A Sprint tem duas partes principais:

- **A Skill:** orienta a instalação, cria a ferramenta e aplica as melhorias solicitadas.
- **A aplicação:** é o arquivo HTML que abre no navegador e reúne os recursos de gestão de tarefas.

Durante a instalação, o bootstrap `scripts/install.py` executa o gerador e cria o artefato `Sprint.html`. O procedimento de instalação só termina depois que o arquivo é criado e verificado.

## Arquitetura

```mermaid
flowchart TB
    USER[Pessoa usuária] --> DOWNLOAD[Baixa o projeto]
    DOWNLOAD --> INSTALL[Instala a Agent Skill]
    INSTALL --> BOOT[Executa scripts/install.py]
    BOOT --> GENERATOR[scripts/create_artifact.py]
    SOURCE[assets/sprint.html<br/>fonte principal] --> GENERATOR
    GENERATOR --> ARTIFACT[Sprint.html<br/>artefato gerado]
    ARTIFACT --> BROWSER[Navegador]
    BROWSER --> UI[Interface da Sprint]
    UI --> LOCAL[(localStorage<br/>do navegador)]
    USER -->|pede melhorias em linguagem natural| SKILL[Agent Skill]
    SKILL -->|edita quando há permissão| SOURCE
    SKILL -->|gera nova versão| GENERATOR
```

## Ciclo de criação e melhoria

```mermaid
flowchart TD
    A[Baixar e instalar a Skill] --> B[Executar o bootstrap]
    B --> C[Gerar Sprint.html]
    C --> D[Usar a ferramenta]
    D --> E{Há pedido de melhoria?}
    E -->|Não| D
    E -->|Sim| F[Interpretar o pedido]
    F --> G[Editar a fonte principal]
    G --> H[Revisar e testar]
    H --> I[Gerar artefato atualizado]
    I --> D
```

A Skill pode trabalhar em linguagem natural: a pessoa descreve o que quer mudar e a Skill transforma o pedido em alterações no código. Quando o ambiente permite salvar a pasta da Skill, a fonte principal fica atualizada para as próximas execuções. Se não houver permissão de escrita, a Skill ainda pode entregar o HTML modificado, mas a fonte do pacote precisará ser atualizada depois.

A geração do arquivo não altera automaticamente uma cópia que já esteja aberta no navegador, nem sincroniza outras instalações. Para usar uma melhoria, abra ou recarregue a nova versão do artefato.

## Como a aplicação funciona

A aplicação é client-side e está concentrada em um único HTML. O arquivo reúne estrutura da página, estilos e JavaScript. Não há etapa de compilação, servidor ou biblioteca JavaScript obrigatória.

### Partes internas

1. **Interface:** telas, cartões, quadro Kanban, cronograma, filtros, modais e temas claro/escuro.
2. **Regras da aplicação:** movimentação das tarefas, datas, sprints, feriados, indicadores de saúde e previsão.
3. **Dados locais:** leitura e gravação no `localStorage` do navegador.
4. **Imagens:** anexos convertidos em Data URL e guardados no armazenamento local.
5. **Geração:** Skill e scripts que produzem uma cópia HTML pronta para abrir.

## Inicialização e dados

- Ao abrir, a aplicação procura os dados salvos no navegador usando a chave `sprint.demo.v1`.
- Se ainda não houver dados válidos, carrega o conjunto fictício `DEMO`.
- A interface apresenta as informações e acompanha as alterações feitas durante o uso.
- As mudanças são salvas no navegador atual.

## O que esta versão não faz

- Não tem backend nem banco de dados remoto.
- Não sincroniza alterações entre pessoas, computadores ou navegadores.
- Não possui login, perfis ou controle de acesso.
- Não oferece backup automático nem recuperação de dados apagados.
- Não atualiza sozinha uma cópia antiga do HTML já aberta ou distribuída.

O `localStorage` é vinculado ao navegador e ao perfil em que a aplicação foi usada. Por isso, não deve ser tratado como armazenamento seguro para senhas, tokens ou informações confidenciais.
