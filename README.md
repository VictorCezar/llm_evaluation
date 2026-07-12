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

### 🔑 Configurando a API Key do Groq (`.env`)
Antes de rodar o projeto localmente, é necessário obter as credenciais da API do Groq.

**Criar a Groq API Key:**
1. Acesse o console oficial do Groq: https://console.groq.com/.
2. Faça login ou crie uma conta gratuita.
3. Vá para a seção **API Keys** no painel lateral.
4. Clique em **Create API Key**, atribua um nome a ela e copie a chave gerada (com formato `gsk_...`).

**Configurar o Arquivo `.env`:**
1. Duplique o arquivo `.env.example` presente na raiz do projeto e renomeie a cópia para `.env`.
   ```bash
   cp .env.example .env
   ```
2. Adicione a chave gerada à variável `GROQ_API_KEY` e configure as demais variáveis básicas:
   ```env
   ENVIRONMENT=development
   PORT=8000
   HOST=0.0.0.0

   GROQ_API_KEY=gsk_suachaveaqui...
   GROQ_MODEL=openai/gpt-oss-120b
   ```

### 📊 Observabilidade com LangSmith (Opcional)
O projeto possui suporte integrado à telemetria e rastreamento das execuções do LLM através do **LangSmith**. No entanto, **o uso do LangSmith é totalmente opcional** e o projeto funciona perfeitamente sem ele.

* **Se você NÃO deseja usar a telemetria:**
  Basta definir `LANGCHAIN_TRACING_V2=false` no seu arquivo `.env`. Com isso, a aplicação funcionará normalmente sem tentar enviar logs ou se conectar aos servidores do LangSmith.
  ```env
  LANGCHAIN_TRACING_V2=false
  LANGCHAIN_API_KEY=
  LANGCHAIN_PROJECT=llm-as-a-judge
  ```

* **Se você deseja ativar a telemetria:**
  1. Crie uma conta no site oficial do [LangSmith](https://smith.langchain.com/).
  2. Vá nas configurações de sua conta, crie uma **API Key** e adicione as variáveis no seu `.env`:
     ```env
     LANGCHAIN_TRACING_V2=true
     LANGCHAIN_API_KEY=sua_chave_do_langsmith_aqui
     LANGCHAIN_PROJECT=llm-as-a-judge
     ```
  3. Ao rodar o projeto, todos os logs e fluxos da função avaliadora serão enviados para a sua conta e poderão ser inspecionados graficamente no painel do LangSmith.

---

## 🐳 Executando com Docker (Recomendado)

O projeto é autossuficiente para deploy e pode ser executado facilmente com Docker Compose.

1. Construa e inicie o contêiner:
   ```bash
   docker compose up --build
   ```
2. A aplicação e seus endpoints estarão disponíveis em:
   * **Painel do Frontend (Dashboard):** `http://localhost:8000/` (Interface gráfica para envio e visualização das análises de conversas em tempo real)
   * **Endpoint de Avaliação da API:** `POST http://localhost:8000/evaluate`
   * **Documentação interativa da API (Swagger UI):** `http://localhost:8000/docs`

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
