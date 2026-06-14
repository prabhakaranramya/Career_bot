import sys, os
sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm_chain import get_career_response
from nlp_processor import extract_intent_and_skills

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    history: list

class ChatResponse(BaseModel):
    reply: str
    intent: str
    skills_mentioned: list

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    intent, skills = extract_intent_and_skills(request.message)
    reply = get_career_response(request.message, request.history)
    return ChatResponse(reply=reply, intent=intent, skills_mentioned=skills)

@app.get("/health")
def health():
    return {"status": "ok"}