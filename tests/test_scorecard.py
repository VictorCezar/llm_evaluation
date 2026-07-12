import pytest
from pydantic import ValidationError
from app.models.scorecard import ConversationRequest, EvaluationCriterion, ScorecardResponse

def test_conversation_request_valid():
    """Test that a valid ConversationRequest is correctly instantiated."""
    req = ConversationRequest(
        sessionId="S_12345",
        messages=["human: Olá", "ai: Como posso ajudar?"]
    )
    assert req.sessionId == "S_12345"
    assert len(req.messages) == 2
    assert req.messages[0] == "human: Olá"

def test_conversation_request_invalid():
    """Test that ConversationRequest raises ValidationError on missing fields or wrong types."""
    with pytest.raises(ValidationError):
        # Missing sessionId
        ConversationRequest(messages=["human: Olá"])
        
    with pytest.raises(ValidationError):
        # Missing messages
        ConversationRequest(sessionId="S_12345")

def test_evaluation_criterion_valid():
    """Test that a valid EvaluationCriterion is correctly instantiated."""
    criterion = EvaluationCriterion(
        score=4,
        justification="Atendimento cordial e atencioso",
        evidence=["ai: Olá, Pessoa_001, eu sou a Beatriz, consultora de carreira..."]
    )
    assert criterion.score == 4
    assert criterion.justification == "Atendimento cordial e atencioso"
    assert criterion.evidence == ["ai: Olá, Pessoa_001, eu sou a Beatriz, consultora de carreira..."]

def test_evaluation_criterion_invalid_score():
    """Test that EvaluationCriterion raises validation errors when score is outside the [1, 5] range."""
    # Score too high
    with pytest.raises(ValidationError):
        EvaluationCriterion(
            score=6,
            justification="Excelente",
            evidence=[]
        )
        
    # Score too low
    with pytest.raises(ValidationError):
        EvaluationCriterion(
            score=0,
            justification="Péssimo",
            evidence=[]
        )

def test_scorecard_response_valid():
    """Test that a valid ScorecardResponse is correctly instantiated."""
    criterion_good = EvaluationCriterion(
        score=5,
        justification="Excelente atendimento, claro e educado",
        evidence=["ai: Olá, como posso ajudar?", "ai: Deixo aberto para avançarmos juntos"]
    )
    criterion_ok = EvaluationCriterion(
        score=4,
        justification="Tirou as dúvidas mas demorou um pouco",
        evidence=["ai: Sobre valores, vou te conectar..."]
    )
    
    scorecard = ScorecardResponse(
        sessionId="S_12345",
        overall_score=4.33,
        identificacao_necessidade=criterion_good,
        aderencia_protocolo=criterion_good,
        controle_alucinacao=criterion_good,
        empatia=criterion_ok,
        feedback_geral="O atendimento foi muito bom no geral."
    )
    assert scorecard.sessionId == "S_12345"
    assert scorecard.overall_score == 4.33
    assert scorecard.identificacao_necessidade.score == 5
    assert scorecard.empatia.score == 4

def test_scorecard_response_invalid_overall_score():
    """Test that ScorecardResponse raises validation errors for invalid overall_score."""
    criterion = EvaluationCriterion(
        score=5,
        justification="Excelente",
        evidence=[]
    )
    
    # Overall score too high
    with pytest.raises(ValidationError):
        ScorecardResponse(
            sessionId="S_12345",
            overall_score=5.5,
            identificacao_necessidade=criterion,
            aderencia_protocolo=criterion,
            controle_alucinacao=criterion,
            empatia=criterion,
            feedback_geral="Excelente"
        )
        
    # Overall score too low
    with pytest.raises(ValidationError):
        ScorecardResponse(
            sessionId="S_12345",
            overall_score=0.5,
            identificacao_necessidade=criterion,
            aderencia_protocolo=criterion,
            controle_alucinacao=criterion,
            empatia=criterion,
            feedback_geral="Péssimo"
        )

