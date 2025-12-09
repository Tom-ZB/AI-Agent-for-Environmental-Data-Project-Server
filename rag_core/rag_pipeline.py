import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.runnables import RunnableMap

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY1")
base_url = os.getenv("OPENAI_BASE_URL")

llm = ChatOpenAI(
    model="gpt-4.1-nano",
    base_url=base_url,
    api_key=api_key,
    max_tokens=2000,
    temperature=0.7
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "If the question relates to the text below, use it:\n{context}\n\nOtherwise, just respond naturally.\n\nQuestion: {question}")
])



# 文档加载与向量库初始化
file_path = "test.txt"
text_loader = TextLoader(file_path, encoding="utf-8")
documents = text_loader.load()

splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)
texts = splitter.split_documents(documents)

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small",
    base_url=base_url,
    api_key=api_key
)

vectorstore = Chroma.from_documents(
    documents=texts,
    embedding=embedding_model,
    # persist_directory="chroma2"
)

retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "score_threshold": 0.5,   # 自定义阈值
        "k": 3
    }
)


#这里字典x实际就是传入的inputs字典 这里就是做了映射
chain = RunnableMap({
    "question": lambda x: x["question"],
    "context": lambda x: x["context"],
    "history": lambda x: x["history"]
}) | prompt | llm

def build_inputs(question: str, history: str):
    docs = retriever.invoke(question)
    context = "\n\n".join(d.page_content for d in docs) if docs else ""
    return {"question": question, "context": context, "history": history}

def convert_history(raw_history):
    msgs = []
    for role, content in raw_history:
        if role.lower() == "user":
            msgs.append(HumanMessage(content=content))
        else:
            msgs.append(AIMessage(content=content))
    return msgs

def run_rag(question: str, history_raw: list):
    # 转换成 LangChain 消息格式
    history = convert_history(history_raw)

    docs = retriever.invoke(question)
    print("RAG docs:", docs)

    if not docs:
        # 无文档 → 纯自然对话
        return llm.invoke([
            ("system", "You are a helpful assistant."),
            *history,
            ("human", question)
        ]).content, ""

    # 有文档 → RAG
    context = "\n\n".join(d.page_content for d in docs)
    inputs = {
        "question": question,
        "context": context,
        "history": history,
    }
    result = chain.invoke(inputs)

    return result.content, context


