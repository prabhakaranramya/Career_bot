import sys, os
from typing import Optional
import sqlite3

sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm_chain import get_career_response
from nlp_processor import extract_intent_and_skills
from database import save_conversation, load_conversation, list_conversations, delete_conversation, DB_PATH

app = FastAPI()

# CORS middleware - must be first
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://192.168.156.46:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PUT"],
    allow_headers=["*"],
    max_age=600,
)

class ChatRequest(BaseModel):
    message: str
    history: list
    user_id: str = "default_user"
    chat_title: str = "New Chat"

class ChatResponse(BaseModel):
    reply: str
    intent: str
    skills_mentioned: list

class ConversationRequest(BaseModel):
    user_id: str = "default_user"

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Handle chat messages and save to database"""
    try:
        intent, skills = extract_intent_and_skills(request.message)
        reply = get_career_response(request.message, request.history)
        
        # Build updated message history
        updated_history = request.history + [
            {"role": "user", "content": request.message},
            {"role": "assistant", "content": reply}
        ]
        
        # Save to database
        save_conversation(request.user_id, request.chat_title, updated_history)
        
        return ChatResponse(reply=reply, intent=intent, skills_mentioned=skills)
    except Exception as e:
        print(f"❌ Error in /chat: {e}")
        return ChatResponse(
            reply=f"Error: {str(e)}", 
            intent="error", 
            skills_mentioned=[]
        )

@app.post("/load-chat")
async def load_chat(request: ConversationRequest):
    """Load a conversation"""
    try:
        user_id = request.user_id
        history = load_conversation(user_id, "New Chat")
        return {"history": history, "status": "ok"}
    except Exception as e:
        print(f"❌ Error loading chat: {e}")
        return {"history": [], "status": "error", "error": str(e)}

@app.get("/conversations/{user_id}")
async def get_conversations(user_id: str):
    """List all conversations for a user"""
    try:
        conversations = list_conversations(user_id)
        return {"conversations": conversations, "status": "ok"}
    except Exception as e:
        print(f"❌ Error fetching conversations: {e}")
        return {"conversations": [], "status": "error", "error": str(e)}

@app.delete("/chat/{user_id}/{chat_title}")
async def delete_chat(user_id: str, chat_title: str):
    """Delete a conversation"""
    try:
        delete_conversation(user_id, chat_title)
        return {"status": "deleted", "message": "Conversation deleted successfully"}
    except Exception as e:
        print(f"❌ Error deleting conversation: {e}")
        return {"status": "error", "error": str(e)}

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "ok", "service": "CareerCompass AI Backend"}

@app.get("/db-stats")
def db_stats():
    """Get database statistics"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("SELECT COUNT(*) FROM conversations")
        total_conversations = c.fetchone()[0]
        
        c.execute("SELECT COUNT(DISTINCT user_id) FROM conversations")
        total_users = c.fetchone()[0]
        
        conn.close()
        
        return {
            "status": "ok",
            "total_conversations": total_conversations,
            "total_users": total_users,
            "database_path": DB_PATH
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}