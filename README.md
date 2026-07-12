# LLM-as-a-Judge - Avaliação de Conversas de Atendimento

Este projeto implementa um sistema de "LLM-as-a-Judge" robusto e assíncrono para avaliar a qualidade de conversas de atendimento ao cliente da +A Code Academy. A aplicação realiza a sanitização de dados sensíveis (PII) antes de enviar a conversa para avaliação por meio da API do Groq (utilizando Pydantic e Instructor para estruturação das saídas) e inclui suporte à observabilidade com LangSmith.

---

## 🚀 Requisitos e Dependências

As principais tecnologias e dependências utilizadas são:
* **Python 3.11+**
* **FastAPI** & **Uvicorn**
* **Instructor** & **Pydantic**
* **Groq API**
* **Microsoft Presidio** (Analyzer e Anonymizer)
* **spaCy** (Modelo `en_core_web_lg`)
* **LangSmith** (Observabilidade e tracing)
* **Docker** & **Docker Compose**
* **Pytest** & **HTTPX** (Para testes automatizados e TDD)

---

## ⚙️ Configuração do Ambiente

1. Clone ou acesse o repositório do projeto.
2. Copie o arquivo de exemplo de ambiente `.env.example` para `.env`:
   ```bash
   cp .env.example .env
   ```
3. Abra o arquivo `.env` e configure as seguintes variáveis:
   ```env
   # Configurações do Servidor
   ENVIRONMENT=development
   PORT=8000
   HOST=0.0.0.0

   # API do Groq
   GROQ_API_KEY=sua_chave_da_groq_aqui
   GROQ_MODEL=llama3-70b-8192

   # Observabilidade LangSmith (Opcional, mas recomendado)
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_API_KEY=sua_chave_do_langsmith_aqui
   LANGCHAIN_PROJECT=llm-as-a-judge
   ```

---

## 🐳 Executando com Docker (Recomendado)

O projeto é autossuficiente para deploy e pode ser executado facilmente com Docker Compose.

1. Construa e inicie o contêiner:
   ```bash
   docker compose up --build
   ```
2. A API estará disponível em:
   * **Endpoint de Avaliação:** `POST http://localhost:8000/evaluate`
   * **Documentação interativa (Swagger UI):** `http://localhost:8000/docs`

---

## 🧪 Executando os Testes Unitários

O desenvolvimento seguiu rigorosamente a metodologia **TDD (Test-Driven Development)**. Para executar os testes unitários utilizando o ambiente virtual local:

1. Ative seu ambiente virtual (se aplicável) e instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute o `pytest`:
   ```bash
   pytest
   ```
   *Os testes cobrem a sanitização de PII (Presidio), parsing de schemas (Pydantic), o serviço de avaliação por LLM e os endpoints FastAPI.*

---

## 🔍 Validação Funcional (test_live.py)

Com a API rodando (seja localmente ou via contêiner Docker na porta 8000), você pode rodar o script de validação funcional para fazer uma requisição real e ver o Scorecard detalhado gerado pelo LLM.

Execute o script na raiz do projeto:
```bash
python test_live.py
```

O script enviará uma conversa de mock real baseada no arquivo `exemplo_conversas.json` e imprimirá no terminal o retorno estruturado (`ScorecardResponse`) com notas de 1 a 5, justificativas detalhadas e as evidências textuais encontradas na conversa.
