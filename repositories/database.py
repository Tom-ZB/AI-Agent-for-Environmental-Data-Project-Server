from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./rag_chat.db"

#创建数据库引擎，管理与数据库的底层连接  check_same_thread这个参数如果是多线程必须要关闭
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
#创建一个会话工厂，后续通过SessionLocal()获取数据库对话对象 用于执行增删改查等操作 autocommit：自动提交 autoflush：自动刷新
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#SQLAlchemy 提供的工厂函数，返回一个“基类”对象
#所有 ORM 模型类都必须继承它，才能被 SQLAlchemy 识别为数据库表的映射
Base = declarative_base()
