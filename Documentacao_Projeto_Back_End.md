# Projeto Multidisciplinar: Raízes do Nordeste - API Back-End

**Curso:** Análise e Desenvolvimento de Sistemas (ADS)
**Disciplina:** Projeto Multidisciplinar / Eletiva IV

---

## 1. Introdução

Este projeto foi desenvolvido para atender aos requisitos da disciplina Projeto Multidisciplinar do curso de Análise e Desenvolvimento de Sistemas. O objetivo foi desenvolver uma API REST para a rede fictícia "Raízes do Nordeste", permitindo o gerenciamento de pedidos, produtos, estoque, pagamentos simulados e programa de fidelidade.

Durante o desenvolvimento foram aplicados conceitos estudados ao longo do curso, como modelagem de banco de dados, criação de APIs utilizando FastAPI, autenticação com JWT, documentação automática por meio do Swagger/OpenAPI e persistência de dados utilizando SQLite.

A proposta do projeto foi desenvolver uma aplicação organizada, funcional e de fácil manutenção, simulando situações encontradas no desenvolvimento de sistemas Back-End.

---

## 2. Análise e Requisitos

Durante o levantamento de requisitos, foram identificadas as principais necessidades do negócio para suportar a operação das filiais.

### Requisitos Funcionais (RF)
* **RF01:** O sistema deve permitir o cadastro e a autenticação de usuários baseada em perfis de acesso (Cliente, Atendente, Cozinha, Gerente).
* **RF02:** O sistema deve manter o cadastro de produtos (Cardápio) padronizados entre todas as filiais.
* **RF03:** O sistema deve registrar pedidos oriundos de múltiplos canais (APP ou PDV).
* **RF04:** O sistema deve garantir a baixa instantânea e consistente no estoque da unidade específica no ato da criação do pedido.
* **RF05:** O sistema não deve permitir o registro de um pedido caso não haja estoque suficiente (Validação e Controle).
* **RF06:** O sistema deve processar o mock de pagamentos associados aos pedidos, garantindo mudança de status.
* **RF07:** O sistema deve acumular pontos no programa de fidelidade para pedidos concluídos.

### Requisitos Não Funcionais (RNF)
* **RNF01 (Desempenho):** A API deve responder às requisições com baixa latência, adequada para operações de frente de caixa.
* **RNF02 (Segurança):** A autenticação deve utilizar tokens JWT (JSON Web Token) e as senhas devem ser salvas criptografadas (Hash Bcrypt).
* **RNF03 (Arquitetura):** O código deve seguir princípios de modularização e separação de responsabilidades (Rotas, Modelos e Schemas).
* **RNF04 (Documentação):** A API deve prover documentação viva via Swagger/OpenAPI.
*

* 

---

## 3. Modelagem e 4. DER (Diagrama de Entidade-Relacionamento)

A modelagem de dados foi desenhada para a estrutura relacional do SQLite, com as chaves estrangeiras devidamente mapeadas visando manter a integridade referencial.
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/7436bea8-f13a-470b-a4b2-be477a7dee5d" />
>
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/65f8146a-eec0-4a43-9065-fadf26a29f95" />





---

## 5. Casos de Uso

As interações sistêmicas foram mapeadas para garantir que as rotas respeitassem o fluxo operacional da tapiocaria:
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/212331b2-8465-4026-9480-51eee0e82d98" />



```

---

## 6. Arquitetura do Sistema

Para o desenvolvimento da API foi utilizada a linguagem Python juntamente com o framework FastAPI. Essa escolha ocorreu devido à facilidade de desenvolvimento de APIs REST, à documentação automática via Swagger/OpenAPI e à organização do projeto.

O SQLAlchemy foi utilizado para realizar o mapeamento entre as classes da aplicação e o banco de dados SQLite, enquanto o Pydantic ficou responsável pela validação dos dados enviados e recebidos pela API.

O projeto foi organizado em módulos, separando as rotas, modelos, esquemas e demais arquivos da aplicação, tornando o código mais organizado e facilitando sua manutenção.

---

## 7. Endpoints

Os serviços expostos pela API foram separados por módulos de negócio:

* **Módulo de Autenticação (`/auth`)**:
  - `POST /auth/registrar`: Cadastro de novos usuários (criptografando senhas).
  - `POST /auth/login`: Autenticação retornando Token JWT (Bearer).
* **Módulo de Produtos (`/produtos`)**:
  - `GET /produtos/`: Consulta aberta do cardápio.
  - `POST /produtos/`: Cadastro restrito a gerentes.
* **Módulo de Pedidos (`/pedidos`)**:
  - `POST /pedidos/`: Rota central. Efetua a criação do carrinho, valida o saldo em estoque, realiza o débito (baixa) no estoque e registra os itens. Requer o preenchimento de `canalPedido` (App ou PDV).
* **Módulo de Pagamentos (`/pagamentos`)**:
  - `POST /pagamentos/`: Simula a liquidação financeira. Salva o registro e acumula pontos.
* **Módulo de Fidelidade (`/fidelidade`)**:
  - `GET /fidelidade/saldo`: Retorna o saldo de pontos atual do usuário.
  - `POST /fidelidade/registrar`: Adiciona pontos ao usuário.
  - `POST /fidelidade/resgatar`: Abate os pontos utilizados, validando o saldo.
* **Módulo de Estoque (`/estoque`)**:
  - `GET /estoque/{unidade_id}`: Permite auditoria da capacidade de insumos por filial.
  - `PATCH /estoque/movimentar`: Realiza entrada/saída de insumos (restrito a ADMIN/GERENTE).

---

## 8. Segurança

Para garantir a segurança da aplicação, foram implementados alguns mecanismos importantes.

As senhas dos usuários são armazenadas utilizando criptografia por meio do algoritmo Bcrypt.
A autenticação da API é realizada utilizando tokens JWT (JSON Web Token).
Os endpoints administrativos verificam o perfil do usuário antes de permitir operações como movimentação de estoque e cadastro de produtos.
As respostas de erro seguem um padrão em formato JSON, facilitando a identificação de problemas durante o uso da API.

---

## 9. Plano de Testes

Os testes garantem a integridade das operações e provam a estabilidade do negócio contra anomalias. Foram realizados testes utilizando a coleção do Postman e um script de testes para validar os principais fluxos da aplicação.

| ID | Funcionalidade / Cenário | Ação (Endpoint) | Status Esperado |
|:---|:---|:---|:---:|
| **T01** | Login Válido | `POST /auth/login` | `200 OK` |
| **T02** | Acesso Restrito sem Token | `GET /pedidos/` | `401 Unauthorized` |
| **T03** | Criação de Pedido sem Campo Canal | `POST /pedidos/` | `422 Unprocessable` |
| **T04** | Criação de Pedido Válido | `POST /pedidos/` | `201 Created` |
| **T05** | Pedido de Produto Inexistente | `POST /pedidos/` | `404 Not Found` |
| **T06** | Integração de Pagamento MOCK Válida | `POST /pagamentos/` | `200 OK` |
| **T07** | Falha no Pagamento MOCK (Recusado) | `POST /pagamentos/` | `400 Bad Request` |
| **T08** | Movimentar Estoque sem Permissão | `PATCH /estoque/movimentar` | `403 Forbidden` |
| **T09** | Consultar Saldo Fidelidade | `GET /fidelidade/saldo` | `200 OK` |
| **T10** | Resgate de Pontos com Saldo Insuficiente | `POST /fidelidade/resgatar` | `400 Bad Request` |
| **T11** | Validação de Estoque Insuficiente | `POST /pedidos/` | `409 Conflict` |

---

## 10. Conclusão

O desenvolvimento deste projeto foi importante para colocar em prática os conteúdos aprendidos durante o curso de Análise e Desenvolvimento de Sistemas.

Durante a implementação foi possível desenvolver uma API REST utilizando FastAPI, criar um banco de dados relacional com SQLite, implementar autenticação utilizando JWT, documentar a aplicação por meio do Swagger/OpenAPI e realizar testes dos principais fluxos da aplicação utilizando o Postman.

Além dos conhecimentos técnicos, o projeto contribuiu para compreender melhor a importância da organização do código, da modelagem de banco de dados e da documentação de sistemas.

Os objetivos propostos pela disciplina foram atingidos, resultando em uma aplicação funcional que atende aos requisitos do estudo de caso e demonstra a aplicação prática dos conteúdos estudados ao longo do curso.
