from fastapi import APIRouter
from models.schemas import QuestionRequest, AnswerResponse
from services.rag_service import process_question

router = APIRouter()

@router.post("/rag", response_model=AnswerResponse)   #使用AnswerResponse 保证返回JSON格式数据
def rag_endpoint(req: QuestionRequest):
    return process_question(req.conversation_id, req.question)
