from fastapi import FastAPI
from controllers import rag_controller
from repositories.database import Base, engine

# 初始化数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(rag_controller.router)
