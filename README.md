# Sistema de Login com Python e MySQL

Sistema de autenticação de usuários com login real em banco de dados, 
utilizando hash de senha, gerenciamento de sessões e cookies.

## 🛠 Tecnologias utilizadas
- Python
- FastHTML
- MySQL
- bcrypt (hash de senha)
- Cookies e sessões (secrets)
- HTML / CSS


![Python](https://img.shields.io/badge/Python-3.11-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0-blue)
![Status](https://img.shields.io/badge/Status-Em%20progresso-yellow)

## ⚙ Funcionalidades
- Cadastro de usuários
- Login com validação em banco de dados
- Armazenamento seguro de senhas com bcrypt
- Criação e controle de sessões
- Cookie com expiração ("lembrar-me")
- Logout com invalidação de sessão

## 🧠 Conceitos aplicados
- Programação Orientada a Objetos
- Separação de responsabilidades (rotas e lógica)
- Segurança de senhas (hash + salt)
- SQL com prepared statements
- Controle de sessão no back-end


## 📁 Estrutura do projeto
- main.py → rotas e controle da aplicação
- logica.py → regras de negócio e banco de dados
- static/ → arquivos estáticos (CSS, imagens)

## ▶ Como executar o projeto

1. Clone o repositório
2. Crie um banco MySQL
3. Configure as credenciais no arquivo de conexão
4. Instale as dependências
5. Execute o projeto

## 📌 Observações
Projeto desenvolvido para fins de estudo e portfólio, 
com foco em autenticação, segurança e back-end.
