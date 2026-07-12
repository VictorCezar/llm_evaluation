from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app
from app.models.scorecard import ScorecardResponse, EvaluationCriterion

client = TestClient(app)

def test_health_endpoint():
    """Verify that the health check endpoint returns 200 and healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_endpoint_success():
    """Verify that the root endpoint GET / returns 200 and HTML content."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Painel de Auditoria de IA" in response.text

def test_root_endpoint_template_not_found():
    """Verify that the root endpoint returns 404 when index.html does not exist."""
    with patch("os.path.exists", return_value=False):
        response = client.get("/")
        assert response.status_code == 404
        assert "Template não encontrado" in response.text


def test_evaluate_endpoint_mocked():
    """Verify that the POST /evaluate endpoint processes requests, calls the services, and returns a scorecard."""
    mock_scorecard = ScorecardResponse(
        sessionId="S_api_123",
        overall_score=4.0,
        identificacao_necessidade=EvaluationCriterion(
            score=4, justification="Boa identificação", evidence=[]
        ),
        aderencia_protocolo=EvaluationCriterion(
            score=4, justification="Adequado", evidence=[]
        ),
        controle_alucinacao=EvaluationCriterion(
            score=4, justification="Adequado", evidence=[]
        ),
        empatia=EvaluationCriterion(
            score=4, justification="Cordial", evidence=[]
        ),
        feedback_geral="Atendimento consistente."
    )
    
    # Mock evaluate_conversation service inside endpoints.py
    with patch("app.api.endpoints.evaluate_conversation", new_callable=AsyncMock) as mock_eval:
        mock_eval.return_value = mock_scorecard
        
        payload = {
            "sessionId": "S_api_123",
            "messages": [
                "human: Olá, meu email é joao@gmail.com. Quero saber sobre pós de IA",
                "ai: Temos a pós RH & IA! Qual seu CPF?"
            ]
        }
        
        response = client.post("/evaluate", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["sessionId"] == "S_api_123"
        assert data["overall_score"] == 4.0
        assert data["identificacao_necessidade"]["score"] == 4
        
        # Verify the service was called
        mock_eval.assert_called_once()
        
        # Check that PII was anonymized before being passed to the evaluator.
        # Since evaluate_conversation was mocked, we check the argument it was called with.
        called_args = mock_eval.call_args[1]
        called_messages = called_args["messages"]
        
        # "joao@gmail.com" should be replaced by "<EMAIL_ADDRESS>" in the conversation passed to evaluator
        assert "joao@gmail.com" not in called_messages[0]
        assert "<EMAIL_ADDRESS>" in called_messages[0]
