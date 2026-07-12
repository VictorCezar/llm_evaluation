from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine
from typing import List

# Initialize Presidio Analyzer and Anonymizer
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# Custom Pattern Recognizer for Brazilian CPF
cpf_pattern = Pattern(
    name="cpf",
    regex=r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b",
    score=0.85
)
cpf_recognizer = PatternRecognizer(
    supported_entity="CPF",
    patterns=[cpf_pattern]
)
analyzer.registry.add_recognizer(cpf_recognizer)

# We focus on the requested entities: CPF, EMAIL_ADDRESS, PHONE_NUMBER, CREDIT_CARD
TARGET_ENTITIES = ["CPF", "EMAIL_ADDRESS", "PHONE_NUMBER", "CREDIT_CARD"]

def anonymize_text(text: str) -> str:
    """
    Anonymizes sensitive PII (CPF, email, phone, credit card) in a single string.
    """
    results = analyzer.analyze(
        text=text,
        language="en",
        entities=TARGET_ENTITIES
    )
    anonymized_result = anonymizer.anonymize(
        text=text,
        analyzer_results=results
    )
    return anonymized_result.text

def anonymize_conversation(messages: List[str]) -> List[str]:
    """
    Anonymizes PII in a list of conversation messages, preserving the 'sender:' prefix.
    """
    anonymized_messages = []
    for msg in messages:
        if ":" in msg:
            sender, content = msg.split(":", 1)
            anonymized_content = anonymize_text(content)
            anonymized_messages.append(f"{sender}:{anonymized_content}")
        else:
            anonymized_messages.append(anonymize_text(msg))
    return anonymized_messages
