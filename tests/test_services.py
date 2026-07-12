import asyncio
from unittest.mock import AsyncMock, patch
from app.services.evaluator import evaluate_conversation
from app.models.scorecard import ScorecardResponse, EvaluationCriterion

def test_evaluate_conversation_mocked():
    """Verify that the evaluator service interacts correctly with Instructor and Groq."""
    mock_response = ScorecardResponse(
        sessionId="S_test_123",
        overall_score=4.5,
        identificacao_necessidade=EvaluationCriterion(
            score=5, justification="Ótimo", evidence=["human: interesse em pós"]
        ),
        aderencia_protocolo=EvaluationCriterion(
            score=4, justification="Seguiu quase tudo", evidence=[]
        ),
        controle_alucinacao=EvaluationCriterion(
            score=5, justification="Não inventou dados", evidence=[]
        ),
        empatia=EvaluationCriterion(
            score=4, justification="Cordial", evidence=[]
        ),
        feedback_geral="Excelente atendimento no geral."
    )
    
    async def run_test():
        with patch("app.services.evaluator.client.chat.completions.create", new_callable=AsyncMock) as mock_create:
            mock_create.return_value = mock_response
            
            result = await evaluate_conversation(
                session_id="S_test_123",
                messages=["human: Olá", "ai: Olá!"]
            )
            
            mock_create.assert_called_once()
            assert result.sessionId == "S_test_123"
            assert result.overall_score == 4.5
            assert result.identificacao_necessidade.score == 5
            assert result.empatia.score == 4
            assert result.feedback_geral == "Excelente atendimento no geral."
            
    asyncio.run(run_test())
