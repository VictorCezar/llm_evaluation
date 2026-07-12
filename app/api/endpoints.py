from fastapi import APIRouter, HTTPException, status
from app.models.scorecard import ConversationRequest, ScorecardResponse
from app.services.anonymizer import anonymize_conversation
from app.services.evaluator import evaluate_conversation

router = APIRouter()

@router.post(
    "/evaluate",
    response_model=ScorecardResponse,
    status_code=status.HTTP_200_OK,
    summary="Avalia uma conversa de atendimento",
    description="Anonimiza dados sensíveis (PII) e avalia a qualidade do atendimento com LLM-as-a-Judge."
)
async def evaluate_endpoint(request: ConversationRequest) -> ScorecardResponse:
    """
    Receives a conversation, anonymizes its content, runs the business criteria evaluation
    via Groq + Instructor, and returns the detailed scorecard.
    """
    try:
        # 1. Anonymize conversation messages
        anonymized_messages = anonymize_conversation(request.messages)
        
        # 2. Call LLM evaluator
        scorecard = await evaluate_conversation(
            session_id=request.sessionId,
            messages=anonymized_messages
        )
        return scorecard
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao avaliar conversa: {str(e)}"
        )
