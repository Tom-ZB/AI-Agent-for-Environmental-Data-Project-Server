from repositories import rag_repository
from rag_core.rag_pipeline import run_rag

def process_question(conversation_id: str, question: str):
    history_raw = rag_repository.get_history_raw(conversation_id) #从数据库中获取对话历史
    answer, context = run_rag(question, history_raw) #这里调用大模型 传入对话历史以及问题 得到答案以及新的上下文
    rag_repository.save_message(conversation_id, "User", question)  #将对话历史存入
    rag_repository.save_message(conversation_id, "Assistant", answer) #将对话历史存入
    return {
        "conversation_id": conversation_id,
        "answer": answer,
        "context": context,
        "history": rag_repository.get_history(conversation_id)
    }
