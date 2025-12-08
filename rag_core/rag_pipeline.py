import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
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
    max_tokens=200,
    temperature=0.7
)

prompt_template = """你是一个基于文档的问答助手。
请使用以下提供的文本内容来回答问题，仅使用提供的文本信息。
如果文本中没有相关的信息，请回答“抱歉，提供的文本中没有这个信息”。

对话历史：
{history}

文本内容：
{context}

问题：{question}

回答：
"""
prompt = PromptTemplate.from_template(prompt_template)

# 文档加载与向量库初始化
file_path = "test.txt"
text_loader = TextLoader(file_path, encoding="utf-8")
documents = text_loader.load()

splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
texts = splitter.split_documents(documents)

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small",
    base_url=base_url,
    api_key=api_key
)

vectorstore = Chroma.from_documents(
    documents=texts,
    embedding=embedding_model,
    persist_directory="chroma2"
)

retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"score_threshold":0.1, "k":3}
)

chain = RunnableMap({
    "question": lambda x: x["question"],
    "context": lambda x: x["context"],
    "history": lambda x: x["history"]
}) | prompt | llm

def build_inputs(question: str, history: str):
    docs = retriever.invoke(question)
    context = "\n\n".join(d.page_content for d in docs) if docs else "（未找到相关内容）"
    return {"question": question, "context": context, "history": history}

def run_rag(question: str, history: str):
    inputs = build_inputs(question, history)
    result = chain.invoke(inputs)
    return result.content, inputs["context"]
