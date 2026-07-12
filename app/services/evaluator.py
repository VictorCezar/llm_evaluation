import groq
import instructor
from langsmith import traceable
from app.core.config import settings
from app.core.prompts import EVALUATION_SYSTEM_PROMPT
from app.models.scorecard import ScorecardResponse
from typing import List

# Setup Groq Async client wrapped with instructor
# (this ensures structural output validation using Pydantic models)
groq_client = groq.AsyncGroq(api_key=settings.GROQ_API_KEY)
client = instructor.from_groq(groq_client)

@traceable(name="Evaluate Conversation")
async def evaluate_conversation(session_id: str, messages: List[str]) -> ScorecardResponse:
    """
    Evaluates an anonymized conversation using Groq and Instructor,
    returning a structured ScorecardResponse.
    """
    conversation_text = "\n".join(messages)
    
    response = await client.chat.completions.create(
        model=settings.GROQ_MODEL,
        response_model=ScorecardResponse,
        messages=[
            {
                "role": "system",
                "content": EVALUATION_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"Session ID: {session_id}\n\nConversation Transcript:\n{conversation_text}"
            }
        ]
    )
    return response
