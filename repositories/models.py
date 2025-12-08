from sqlalchemy import Column, Integer, String, Text
from .database import Base

# 这段代码定义了一个使用 SQLAlchemy 的 ORM 模型，它把 Python 类映射到数据库中的一张表，用于持久化每条对话消息。实例代表表中的一行记录，字段对应列，便于查询、插入和更新。
# 因为这个类继承了Base 因此SQLAlchemy 知道有一张叫 conversation_history 的表，并且知道它的列结构
#当你调用 Base.metadata.create_all(bind=engine) 时，SQLAlchemy 会扫描所有继承了 Base 的类，并在数据库里创建对应的表（所有继承了Base的类就相当于一张张table）
class ConversationHistory(Base):
    __tablename__ = "conversation_history"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String, index=True)   # 会话ID
    role = Column(String)                          # 用户/助手
    content = Column(Text)                         # 消息内容
