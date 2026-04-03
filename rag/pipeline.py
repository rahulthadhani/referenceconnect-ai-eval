import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

DOCS_DIR = Path("data/documents")
VECTORSTORE_DIR = "vectorstore"


def load_documents():
    docs = []
    for path in DOCS_DIR.glob("*.txt"):
        loader = TextLoader(str(path), encoding="utf-8")
        loaded = loader.load()
        for doc in loaded:
            doc.metadata["source"] = path.name
        docs.extend(loaded)
    print(f"[OK] Loaded {len(docs)} documents")
    return docs


def build_vectorstore(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    print(f"[OK] Split into {len(chunks)} chunks")

    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(
        chunks, embeddings, persist_directory=VECTORSTORE_DIR
    )
    print(f"[OK] Vectorstore built and saved to {VECTORSTORE_DIR}/")
    return vectordb


def load_vectorstore():
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory=VECTORSTORE_DIR, embedding_function=embeddings)
    return vectordb


def build_qa_chain(vectordb):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    prompt = ChatPromptTemplate.from_template(
        """
You are a helpful assistant. Answer the question using only the context provided.
If the answer is not in the context, say "I don't have enough information to answer that."

Context:
{context}

Question: {question}
"""
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain, retriever


if __name__ == "__main__":
    docs = load_documents()
    vectordb = build_vectorstore(docs)
    print("\n[OK] Pipeline ready. Vectorstore built successfully.")
