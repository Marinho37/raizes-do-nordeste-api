# Raízes do Nordeste - API Back-End

Este repositório contém a implementação da API de Back-End para o Projeto Multidisciplinar "Raízes do Nordeste". A solução foi desenvolvida em Python 3 utilizando o framework FastAPI, SQLite para banco de dados relacional leve e SQLAlchemy como ORM.

## Requisitos
- Python 3.9+
- SQLite (Nativo do Python)
- Bibliotecas do `requirements.txt`

## Configurando Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto baseado no `.env.example`:
```env
SECRET_KEY=sua_chave_secreta_super_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Como executar

1. Clone o repositório ou acesse a pasta raiz do projeto.
2. Crie um ambiente virtual (recomendado):
   ```bash
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```
3. Instale as dependências:
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic email-validator bcrypt python-jose[cryptography]
   # ou via arquivo se gerado: pip install -r requirements.txt
   ```
4. Banco de Dados, Migrations e Seed:
   O banco SQLite (`raizes_nordeste.db`) será criado automaticamente com todas as tabelas (via `Base.metadata.create_all`) assim que a API rodar pela primeira vez. Não é necessário comando extra para *migrations* em ambiente acadêmico simplificado.
5. Inicie a API com o Uvicorn:
   ```bash
   uvicorn app.main:app --reload
   ```

## Swagger e Documentação
- **Acesse o Swagger interativo:** http://localhost:8000/docs
- **Acesse o Redoc:** http://localhost:8000/redoc

## Como rodar os Testes
Para testar a aplicação, importamos o arquivo `test_api.py` na raiz, e incluímos a coleção do Postman.
1. Script de testes automatizado (Executa os 10 cenários e levanta o servidor temporariamente):
   ```bash
   python test_api.py
   ```
2. Coleção Postman `Raizes_do_Nordeste_Postman_Collection.json`:
   Abra o Postman, vá em `Import` e selecione o arquivo. Em seguida preencha a variável global `{{token}}` com o token gerado no Request "Login válido" e execute a coleção.
