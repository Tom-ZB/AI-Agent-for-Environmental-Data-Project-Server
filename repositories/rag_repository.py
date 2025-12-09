from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import ConversationHistory

def save_message(conversation_id: str, role: str, content: str):
    db: Session = SessionLocal()
    message = ConversationHistory(conversation_id=conversation_id, role=role, content=content)
    db.add(message)
    db.commit()
    db.close()

# Get chat_history from database
def get_history(conversation_id: str):
    db: Session = SessionLocal()
    messages = db.query(ConversationHistory).filter(
        ConversationHistory.conversation_id == conversation_id
    ).all()
    db.close()
    return "\n".join([f"{m.role}: {m.content}" for m in messages]) if messages else ""


def get_history_raw(conversation_id: str):
    db: Session = SessionLocal()
    messages = (
        db.query(ConversationHistory)
        .filter(ConversationHistory.conversation_id == conversation_id)
        .all()
    )
    db.close()
    return [(m.role, m.content) for m in messages]


