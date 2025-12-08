from pydantic import BaseModel

class QuestionRequest(BaseModel):
    conversation_id: str
    question: str

class AnswerResponse(BaseModel):
    conversation_id: str
    answer: str
    context: str
    history: str
