# Raízes do Nordeste - API Back-End

API REST desenvolvida como Projeto Multidisciplinar da disciplina de Projeto Multidisciplinar – Trilha Back-End do curso superior de Análise e Desenvolvimento de Sistemas.

## 1. Nome do Projeto e Objetivo
Este repositório contém a implementação da API de Back-End para o Projeto Multidisciplinar "Raízes do Nordeste". O objetivo é prover uma API REST para gerenciamento de pedidos, produtos, estoque, controle de pagamentos e programa de fidelidade de uma rede de tapiocarias.

## 2. Tecnologias Utilizadas
- **Linguagem:** Python 3.9+
- **Framework Web:** FastAPI
- **Banco de Dados:** SQLite (utilizado como banco de dados da aplicação)
- **ORM:** SQLAlchemy
- **Validação de Dados:** Pydantic
- **Autenticação:** JWT (JSON Web Token) e Bcrypt (Hash de Senha)

## 3. Requisitos
- Python 3.9+ instalado
- SQLite (utilizado como banco de dados da aplicação)

## 4. Como configurar o `.env`
Crie um arquivo `.env` na raiz do projeto baseado no `.env.example`:
```env
SECRET_KEY=sua_chave_secreta_super_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 5. Como instalar dependências
1. Clone o repositório ou acesse a pasta raiz do projeto.
2. Crie um ambiente virtual (recomendado):
   ```bash
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```
3. Instale as bibliotecas necessárias:
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic email-validator bcrypt python-jose[cryptography] requests
   ```

## 6. Como iniciar a API
O banco SQLite (raizes_nordeste.db) é criado automaticamente na primeira execução da aplicação.

Inicie o servidor de desenvolvimento utilizando o módulo Uvicorn:
```bash
python -m uvicorn app.main:app --reload
```
O servidor estará ativo localmente na porta 8000.

## 7. Como acessar o Swagger
Com o servidor rodando, a documentação interativa para testar os endpoints (padrão OpenAPI) estará disponível em:
👉 **Swagger:** http://localhost:8000/docs
👉 **ReDoc:** http://localhost:8000/redoc

## 8. Como rodar os testes
Opção 1: **Script Automatizado (Python)**
Rode o script que testa os 11 cenários de sucesso e falha de estoque/autenticação:
```bash
python test_api.py
```

Opção 2: **Coleção Postman**
1. Localize o arquivo `Raizes_do_Nordeste_Postman_Collection.json` na raiz deste repositório.
2. Abra o Postman e clique em **Import** para selecionar o arquivo.
3. Execute o `POST /auth/login` (Login Válido) primeiro.
4. Copie o `access_token` e coloque na variável `token` do Postman para liberar as demais rotas restritas.

## 9. Estrutura do Projeto
```text
raizes_nordeste_api/
├── app/
│   ├── main.py          # Arquivo principal que inicia a aplicação
│   ├── auth.py          # Regras de segurança (JWT/Bcrypt)
│   ├── database.py      # Conexão com SQLite e ORM
│   ├── models.py        # Modelos das tabelas do Banco de Dados
│   ├── schemas.py       # Pydantic (Validação de Entrada/Saída)
│   └── routers/         # Controladores divididos por endpoints (pedidos, produtos, etc.)
├── Raizes_do_Nordeste_Postman_Collection.json # Importar no Postman
├── Documentacao_Projeto_Back_End.md           # Documentação técnica do projeto
├── test_api.py          # Script de testes HTTP
├── .env.example         # Exemplo de variáveis de ambiente
└── README.md            # Este arquivo
```

## 10. Fluxo Principal Implementado

Fluxo A — Pedido → Pagamento Mock → Atualização de Status

- Login do usuário
- Criação do pedido
- Validação do estoque
- Processamento do pagamento Mock
- Atualização do status do pedido
- Persistência em banco SQLite

---

# Evidências

## Repositório Git

https://github.com/Marinho37/raizes-do-nordeste-api

## Documentação Swagger

Após iniciar a API:

http://localhost:8000/docs

## ReDoc

http://localhost:8000/redoc

## Coleção Postman

Arquivo:

Raizes_do_Nordeste_Postman_Collection.json

## Documentação Técnica

Arquivo:

Documentacao_Projeto_Back_End.md

## DER

O DER encontra-se na documentação técnica do projeto.
