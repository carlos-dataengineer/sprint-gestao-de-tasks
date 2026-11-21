# Segurança

## Como a Sprint funciona hoje

A Sprint é um arquivo HTML que roda no navegador. Nesta versão, não tem servidor, login, controle de acesso multiusuário nem envio de dados para serviços externos. As informações e imagens ficam no armazenamento local do navegador.

Por isso, não use esta versão para guardar senhas, tokens, chaves de API ou informações pessoais e empresariais confidenciais. O armazenamento local não é um cofre seguro e pode ser apagado pelo navegador ou pela própria pessoa usuária.

## Como comunicar um problema

Se encontrar uma falha de segurança, evite publicar detalhes que permitam explorá-la em uma issue pública. Entre em contato pelo perfil do mantenedor: [@carlos-dataengineer](https://github.com/carlos-dataengineer). Inclua os passos para reproduzir o problema, o impacto e a versão afetada. Não envie dados reais ou confidenciais.

## Recomendações

- Revise o código antes de executar versões modificadas.
- Mantenha o navegador e o sistema atualizados.
- Não use versões derivadas como serviço compartilhado sem implementar segurança no servidor.
- Não considere o perfil do navegador um mecanismo de autenticação ou autorização.
