import os

# Force Hugging Face / Transformers to use Lambda writable storage
os.environ["HOME"] = "/tmp"
os.environ["HF_HOME"] = "/tmp/huggingface"
os.environ["TRANSFORMERS_CACHE"] = "/tmp/huggingface"
os.environ["SENTENCE_TRANSFORMERS_HOME"] = "/tmp/huggingface"
os.environ["TORCH_HOME"] = "/tmp/torch"

from dotenv import load_dotenv
load_dotenv(override=True)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mangum import Mangum

from chatbot import HealthyKidsChatbot, DEFAULT_FAQ_PATH

app = FastAPI(
    title="Healthy Kids Chatbot API",
    description="HealthyKids chatbot API",
    version="1.0.0"
)

ALLOWED_ORIGINS = os.environ.get(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,https://iteration2.healthykids.live,https://healthykids.live"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in ALLOWED_ORIGINS],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

USE_LLM = os.environ.get("USE_LLM", "false").lower() == "true"

chatbot_instance = None


def get_chatbot():
    global chatbot_instance

    if chatbot_instance is None:
        chatbot_instance = HealthyKidsChatbot(
            faq_file=DEFAULT_FAQ_PATH,
            use_llm=USE_LLM,
            top_k=3
        )

    return chatbot_instance


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
    chatbot = get_chatbot()
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


handler = Mangum(app)