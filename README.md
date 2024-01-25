# Discord Bot para Comunidade de Designers

## Descrição

Este bot foi criado para oferecer suporte e gerenciar uma comunidade de cursos destinada a Designers. O projeto foi desenvolvido para atender às necessidades específicas do servidor, proporcionando uma dinâmica única para os alunos.

## Recursos Principais

- **Controle de Cursos:** O bot oferece recursos específicos para o gerenciamento de cursos, fornecendo informações relevantes e interações específicas para os participantes.

- **Integração com Banco de Dados MYSQL:** O bot possui uma integração eficiente com um banco de dados MYSQL próprio, garantindo a persistência e recuperação de dados essenciais para o funcionamento da comunidade.

- **Integração com API da Kiwify:** Utilizando a API da Kiwify, o bot realiza consultas e atualizações de dados em tempo real, proporcionando uma experiência mais dinâmica e atualizada para os membros da comunidade.

- **Controle Padrão do Discord:** Além das funcionalidades específicas, o bot realiza o controle padrão de um bot Discord, incluindo moderação, gerenciamento de canais e permissões.

- **Gerenciamento de Tickets de Suporte:** Facilita o suporte ao usuário por meio de um sistema de tickets, proporcionando uma abordagem organizada e eficiente para lidar com as solicitações dos membros.

- **Sistema de pontuação por interação:** Criamos uma dinâmica diferente, fazendo com que os usuários sejam bonificados de acordo com sua interação em nosso servidor!

- **Sistema de anúncios e avisos de midias sociais:** O BOT foi integrado com um sistema de notificação (anúncios) de publicações em outras plataformas (Youtube e Instagram até o momento).

## Como Usar

1. **Requisitos:**
   - Ter permissões de administrador no servidor.
   - Configurar corretamente as credenciais do banco de dados MYSQL.
   - Configurar as credenciais da API da Kiwify, se aplicável.

2. **Configuração:**
   - Configure as permissões do bot no servidor.
   - Certifique-se de que as credenciais do banco de dados e da API da Kiwify estejam corretamente configuradas no código do bot.

# Comandos Abertos do Bot

## clear
- Descrição: Limpa mensagens do chat.
- Uso: `/clear qnt=<quantidade> embed=<True/False>`

## consultar
- Descrição: Consulta dados de um aluno.
- Uso: `/consultar aluno=<@aluno> tipo=<True/False>`

## lock
- Descrição: Trava o canal selecionado.
- Uso: `/lock`

## unlock
- Descrição: Destrava o canal selecionado.
- Uso: `/unlock`

## closeticket
- Descrição: Fecha um ticket aberto.
- Uso: `/closeticket`

---

**Observação:** Certifique-se de que o usuário tem permissões de administrador para executar esses comandos. Veja a documentação específica para mais detalhes sobre cada comando.
*Este é um resumo. Consulte a documentação completa para detalhes sobre parâmetros e uso específicos de cada comando.*

## Autores

- João Henrique Mendes de Oliveira

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE.md](LICENSE.md) para detalhes.