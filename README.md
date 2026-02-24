

🚀 Invest-Genius V3: Motor de Recomendação & Simulador Financeiro

Este projeto é um sistema de simulação de investimentos desenvolvido para o ecossistema bancário, focado na experiência do usuário (UX) e na integridade dos dados. Ele permite o cadastro de perfis de investidores, recomenda ativos com base em tolerância de risco e simula o rendimento de juros compostos ao longo do tempo.
🛠️ Tecnologias Utilizadas

    Python 3.10+: Linguagem core do projeto.

    PostgreSQL: Persistência de dados relacional.

    Psycopg2: Driver de conexão entre Python e Banco de Dados.

    NamedTuples: Para garantir a imutabilidade das regras de negócio (ativos).

📌 Funcionalidades

    Gestão de Usuários: Cadastro com validação de maioridade e perfil de risco (1 a 4).

    Motor de Recomendação: Filtra investimentos do catálogo que se adequam à tolerância de perda do cliente.

    Simulador de Tempo: Algoritmo de juros compostos (M=P(1+i)t) que projeta o crescimento do patrimônio.

    Persistência em DB: Integração completa com PostgreSQL para salvar perfis e carteiras de ativos.

🏗️ Estrutura do Banco de Dados

O projeto utiliza um modelo relacional para separar os dados sensíveis dos clientes das suas movimentações financeiras:
