from repositories import rag_repository
from rag_core.rag_pipeline import run_rag

def process_question(conversation_id: str, question: str):
    history = rag_repository.get_history(conversation_id)
    answer, context = run_rag(question, history)
    rag_repository.save_message(conversation_id, "用户", question)
    rag_repository.save_message(conversation_id, "助手", answer)
    return {
        "conversation_id": conversation_id,
        "answer": answer,
        "context": context,
        "history": rag_repository.get_history(conversation_id)
    }
