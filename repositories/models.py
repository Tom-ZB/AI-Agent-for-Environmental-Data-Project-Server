from sqlalchemy import Column, Integer, String, Text
from .database import Base

class ConversationHistory(Base):
    __tablename__ = "conversation_history"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String, index=True)   # 会话ID
    role = Column(String)                          # 用户/助手
    content = Column(Text)                         # 消息内容
