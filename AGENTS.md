# AGENTS.md - Spec Driven Development (LLM-as-a-Judge)

## 1. Contexto e Objetivo
Você é um Engenheiro de IA e Desenvolvedor Backend Sênior. Sua tarefa é codificar um sistema de "LLM-as-a-Judge" para avaliar conversas de atendimento, retornando scores, justificativas e evidências.
A aplicação deve ser robusta, escalável e seguir rigorosamente as boas práticas de engenharia de software e a estrutura de pastas fornecida.

## 2. Stack Tecnológica
* **Linguagem & Framework:** Python 3.11+ e FastAPI (assíncrono, alta performance).
* **Validação e Estruturação:** Pydantic (para schemas de entrada/saída) e Instructor (para garantir a saída estruturada do LLM).
* **Modelo/LLM:** API do Groq (utilizando modelos compatíveis e rápidos, configurado via variável de ambiente `GROQ_API_KEY`).
* **Proteção de Dados Sensíveis (PII):** Microsoft Presidio (sanitização do texto antes de enviar ao LLM).
* **Observabilidade:** LangSmith (configurado via variáveis `LANGCHAIN_TRACING_V2`, `LANGCHAIN_API_KEY`, `LANGCHAIN_PROJECT`).
* **Infraestrutura:** Docker e Docker Compose.

## 3. Diretrizes de Desenvolvimento (Regras Invioláveis)
* **Test-Driven Development (TDD):** Nenhuma entrega, rota ou serviço deve ser considerado concluído sem a implementação de testes unitários robustos e passando utilizando `pytest`. Os testes devem cobrir os casos de sucesso e tratamento de erros.
* **Isolamento de Responsabilidades:** Rotas FastAPI (`api/`) não devem conter lógica de LLM. Toda a integração com Groq, Instructor e Presidio deve ficar isolada em `services/`.
* **Tipagem e Schemas:** Utilize *type hints* rigorosamente em 100% do código. Defina o "Scorecard" da avaliação claramente nos `models/` usando Pydantic.
* **Autossuficiência de Deploy:** A aplicação deve subir completamente funcional com um simples `docker compose up --build`. O `docker-compose.yml` deve expor a porta da API e mapear o arquivo `.env`.

## 4. Estrutura do Projeto
Siga estritamente a seguinte estrutura de diretórios para implementar o código:

├── app/
│   ├── api/          # Endpoints do FastAPI (ex: rotas para receber as conversas)
│   ├── core/         # Configurações globais (Pydantic BaseSettings, carregamento do .env, prompts base)
│   ├── models/       # Schemas Pydantic (Entrada da requisição e Saída do Scorecard)
│   ├── services/     # Lógica core (Integração com Groq + Instructor, sanitização com Presidio)
├── tests/            # Testes unitários com pytest para API, serviços e modelos
├── Dockerfile        # Imagem enxuta (ex: python:3.11-slim) otimizada para FastAPI
├── docker-compose.yml# Orquestração do container, repassando o .env para a aplicação
├── README.md         # Documentação de como configurar a GROQ_API_KEY, rodar o Docker e executar os testes
└── pyproject.toml    # Gerenciamento de dependências modernas (preferencial) ou requirements.txt

## 5. Fluxo de Execução da API
1. O endpoint (FastAPI) recebe um payload JSON contendo uma conversa de atendimento.
2. O serviço de proteção (Presidio) analisa o texto e mascara informações sensíveis (PII).
3. O serviço de avaliação monta o *system prompt* com as regras e aciona a API do Groq (envelopada pelo Instructor) passando a conversa anonimizada.
4. O LangSmith registra o tracing da chamada automaticamente para observabilidade.
5. O Instructor garante que o Groq retorne um JSON perfeitamente alinhado ao modelo Pydantic do Scorecard.
6. A API retorna a avaliação estruturada para o cliente com o HTTP Status correto.