from dotenv import load_dotenv
load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import logging

from vector_store import create_vector_store
from rag_pipeline import search_documents
from gemini_service import generate_ai_requirements
from pdf_export import create_pdf


# ───────── LOGGING ─────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ───────── STARTUP ─────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("App starting...")

    try:
        create_vector_store()
        logger.info("Vector store loaded")
    except Exception as e:
        logger.error(f"Vector store error: {e}")

    yield

    logger.info("App shutting down")


app = FastAPI(title="BRD API", version="0.1.0", lifespan=lifespan)


# ───────── CORS ─────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ───────── MODELS ─────────
class ProjectInput(BaseModel):
    title: str = Field(..., min_length=1)
    domain: str = Field(..., min_length=1)
    features: str = Field(..., min_length=1)


class QuestionInput(BaseModel):
    question: str


# ───────── HEALTH ─────────
@app.get("/")
def home():
    return {"status": "OK"}


# ───────── GENERATE BRD ─────────
@app.post("/generate")
def generate(data: ProjectInput):

    try:
        result = generate_ai_requirements(
            data.title,
            data.domain,
            data.features
        )

        return result   # ✅ FIXED

    except Exception as e:
        logger.exception("Generate failed")
        raise HTTPException(status_code=500, detail=str(e))


# ───────── PDF EXPORT ─────────
@app.post("/export-pdf")
def export_pdf(data: ProjectInput):

    try:
        result = generate_ai_requirements(
            data.title,
            data.domain,
            data.features
        )

        file_path = create_pdf(result["generated_requirement"])  # ✅ FIXED

        return {
            "message": "PDF created",
            "file": file_path
        }

    except Exception as e:
        logger.exception("PDF failed")
        raise HTTPException(status_code=500, detail=str(e))


# ───────── ASK ─────────
@app.post("/ask")
def ask(data: QuestionInput):

    q = data.question.lower()

    rules = {
        "functional": "Functional requirements define system behavior.",
        "non functional": "Non-functional requirements define performance, security.",
        "user story": "As a user, I want X so that Y.",
        "use case": "Use case describes system interaction steps.",
        "acceptance": "Acceptance criteria define completion conditions."
    }

    for key, ans in rules.items():
        if key in q:
            return {"answer": ans}

    try:
        results = search_documents(data.question)
        if results:
            return {"answer": results[0]}
    except:
        pass

    return {"answer": "No specific answer found."}


# ───────── RAG SEARCH ─────────
@app.post("/rag-search")
def rag_search(data: QuestionInput):

    try:
        results = search_documents(data.question)

        return {
            "question": data.question,
            "results": results
        }

    except Exception as e:
        logger.exception("RAG failed")
        raise HTTPException(status_code=500, detail=str(e))