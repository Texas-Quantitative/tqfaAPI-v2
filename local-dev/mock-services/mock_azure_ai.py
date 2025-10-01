"""
Mock Azure AI Foundry Service for Local Development
Following Copilot Instructions: Fast iteration without Azure dependencies
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from typing import List, Dict, Any

app = FastAPI(title="Mock Azure AI Service", version="1.0.0")

class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]
    model: str = "gpt-4o-mini"
    temperature: float = 0.7

class ChatResponse(BaseModel):
    id: str = "mock-chat-response"
    choices: List[Dict[str, Any]]
    usage: Dict[str, int]

@app.post("/chat/completions", response_model=ChatResponse)
async def mock_chat_completion(request: ChatRequest):
    """Mock Azure OpenAI chat completion for local development."""
    
    # Simulate realistic AI response based on input
    user_message = request.messages[-1].get('content', 'No message') if request.messages else 'No message'
    
    mock_response = {
        "id": "mock-chat-123",
        "choices": [{
            "message": {
                "role": "assistant", 
                "content": f"Mock AI response to: {user_message}"
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": len(user_message.split()) if user_message else 0,
            "completion_tokens": 20, 
            "total_tokens": len(user_message.split()) + 20 if user_message else 20
        }
    }
    
    return ChatResponse(**mock_response)

@app.get("/health")
async def health_check():
    """Health check for mock service."""
    return {
        "status": "healthy", 
        "service": "mock-azure-ai", 
        "version": "1.0.0",
        "endpoints": ["/chat/completions", "/health"]
    }

@app.get("/")
async def root():
    """Root endpoint for mock AI service."""
    return {
        "service": "Mock Azure AI Foundry Service",
        "purpose": "Fast local development without Azure dependencies",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat/completions",
            "health": "/health"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001, reload=True)
