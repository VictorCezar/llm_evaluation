from pydantic import BaseModel, Field, AliasChoices
from typing import List

class ConversationRequest(BaseModel):
    """
    Schema for the input request containing the customer service conversation messages.
    Each message in the list should follow the format 'sender: message' (e.g. 'human: Hello' or 'ai: Hi').
    """
    sessionId: str = Field(
        ..., 
        description="Unique identifier for the session/conversation"
    )
    messages: List[str] = Field(
        ..., 
        description="List of messages in the conversation format 'sender: message'"
    )

class EvaluationCriterion(BaseModel):
    """
    Schema for evaluating a specific criterion of the customer service.
    """
    score: int = Field(
        ..., 
        description="Score given to the criterion, ranging from 1 (poor) to 5 (excellent). Use this exact key 'score' (do not translate to 'nota').",
        ge=1,
        le=5,
        validation_alias=AliasChoices('score', 'nota')
    )
    justification: str = Field(
        ..., 
        description="Detailed justification for the assigned score based on the conversation context. Use this exact key 'justification' (do not translate to 'justificativa').",
        validation_alias=AliasChoices('justification', 'justificativa')
    )
    evidence: List[str] = Field(
        ..., 
        description="Exact quotes or references extracted from the conversation that prove/support the score. Use this exact key 'evidence' (do not translate to 'evidencias').",
        validation_alias=AliasChoices('evidence', 'evidencias')
    )

class ScorecardResponse(BaseModel):
    """
    Comprehensive evaluation scorecard for a support conversation.
    """
    sessionId: str = Field(
        ..., 
        description="The session identifier of the evaluated conversation"
    )
    overall_score: float = Field(
        ..., 
        description="Overall average score or global rating for the conversation",
        ge=1.0,
        le=5.0
    )
    identificacao_necessidade: EvaluationCriterion = Field(
        ..., 
        description="Avaliação de quão bem o atendente identificou as necessidades do cliente"
    )
    aderencia_protocolo: EvaluationCriterion = Field(
        ..., 
        description="Avaliação da aderência do atendente aos protocolos e scripts recomendados"
    )
    controle_alucinacao: EvaluationCriterion = Field(
        ..., 
        description="Avaliação de quão preciso foi o atendente em evitar informações falsas ou não confirmadas (alucinações)"
    )
    empatia: EvaluationCriterion = Field(
        ..., 
        description="Avaliação da empatia, escuta ativa e cordialidade no atendimento"
    )
    feedback_geral: str = Field(
        ..., 
        description="General feedback summarizing strengths and improvement areas"
    )

