import sys, os
sys.path.append(os.path.dirname(__file__))

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

SYSTEM_PROMPT = """You are Aria, a friendly and expert career coach and skill development guide.
Your role is to help users:
- Discover the right career path based on their interests and strengths
- Identify skill gaps and how to close them
- Create personalised learning roadmaps with real resources
- Set realistic short-term and long-term career goals
- Recommend courses, certifications, and projects

Your conversation style:
- Ask ONE focused question at a time — never overwhelm the user
- Be encouraging, warm, and practical
- Give specific, actionable advice
- Reference real platforms (Coursera, Udemy, LinkedIn Learning, YouTube)
- When you have enough info, generate a clear step-by-step roadmap
- Keep responses to 3-5 sentences unless generating a roadmap

Always start by asking about the user's current situation if not mentioned."""

def get_career_response(user_message: str, history: list) -> str:
    llm = ChatOllama(model="llama3.2", temperature=0.7)

    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))

    messages.append(HumanMessage(content=user_message))

    response = llm.invoke(messages)
    return response.content