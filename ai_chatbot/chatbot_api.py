import os
from dotenv import load_dotenv

load_dotenv(override=True)

from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import HealthyKidsChatbot, DEFAULT_FAQ_PATH

app = FastAPI(
    title="Healthy Kids Chatbot API",
    description="API for answering parent questions using FAQ retrieval and optional Claude rewriting.",
    version="1.0.0"
)


USE_LLM = os.environ.get("USE_LLM", "true").lower() == "true"


chatbot = HealthyKidsChatbot(
    faq_file=DEFAULT_FAQ_PATH,
    use_llm=USE_LLM,
    top_k=3
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {
        "success": True,
        "message": "Healthy Kids Chatbot API is running.",
        "llm_mode": USE_LLM
    }


@app.post("/chat")
def chat(request: ChatRequest):
    result = chatbot.get_response(request.message)

    return {
        "success": True,
        "message": result["user_input"],
        "reply": result["answer"],
        "intent": result["predicted_intent"],
        "confidence": result["intent_confidence"],
        "matched_question": result["matched_question"],
        "similarity_score": result["similarity_score"]
    }