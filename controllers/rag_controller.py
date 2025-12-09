from fastapi import APIRouter
from models.schemas import QuestionRequest, AnswerResponse
from services.rag_service import process_question

router = APIRouter()

@router.post("/rag", response_model=AnswerResponse)   #使用AnswerResponse 保证返回JSON格式数据
def rag_endpoint(req: QuestionRequest):
    return process_question(req.conversation_id, req.question)


@router.get("/")
def test():
    try:
        # print("called")
        return {"message": "hello"}
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        # print traceback to the server logs for debugging
        print(tb)
        # return error details so the client can see what's failing (for local debugging)
        return {"error": str(e), "traceback": tb}
