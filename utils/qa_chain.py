# file: utils/qa_chain.py
import os
import pickle
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
import requests

load_dotenv()

class OpenRouterLLM(LLM):
    model: str = "deepseek/deepseek-chat-v3-0324:free"
    # model: str = "microsoft/phi-4-reasoning-plus:free"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise RuntimeError("Missing OpenRouter API key.")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        body = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
        data = response.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        else:
            raise RuntimeError(f"API Error: {data}")

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"model": self.model}

    @property
    def _llm_type(self) -> str:
        return "openrouter"


def save_faiss_index(db, path="faiss_index.pkl"):
    with open(path, "wb") as f:
        pickle.dump(db, f)


def load_faiss_index(path="faiss_index.pkl"):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return None


def setup_chain():
    db = load_faiss_index()
    if db is None:
        loader = PyPDFLoader("the-great-gatsby.pdf")
        pages = loader.load_and_split()
        splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=500)
        texts = splitter.split_documents(pages)

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"}
        )
        db = FAISS.from_documents(texts, embeddings)
        save_faiss_index(db)

    retriever = db.as_retriever(search_kwargs={"k": 3})
    return RetrievalQA.from_chain_type(llm=OpenRouterLLM(), retriever=retriever, return_source_documents=True)
