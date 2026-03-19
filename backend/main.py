# main.py
# Simple RAG API with basic auth

import os
import traceback
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from fetch_papers import fetch_papers
from process_papers import load_and_process_papers
from vector_store import create_vector_store, search_vector_store, INDEX_FILE
from chunk_model import Chunk
from llm import generate_answer
from simple_auth import login_simple, verify_token

app = FastAPI(title="Research RAG API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class LoginRequest(BaseModel):
    email: str
    password: str

class TopicRequest(BaseModel):
    topic: str
    max_results: int = 5

class QueryRequest(BaseModel):
    query: str
    top_k: int = 6

# ============ LOGIN ============
@app.post("/login")
def login(req: LoginRequest):
    """Login with email and password"""
    try:
        result = login_simple(req.email, req.password)
        return {
            "status": "success",
            "access_token": result["access_token"],
            "token_type": "bearer"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Login failed")

# ============ PROTECTED ROUTES ============
def get_auth_token(authorization: str = Header(None)) -> str:
    """Extract token from Authorization header"""
    if not authorization:
        raise HTTPException(status_code=401, detail="No token provided")
    
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid token format")
    
    token = parts[1]
    verify_token(token)  # This will raise HTTPException if invalid
    return token

@app.post("/fetch_papers")
def fetch(req: TopicRequest, authorization: str = Header(None)):
    """Fetch and index papers (requires auth)"""
    try:
        get_auth_token(authorization)  # Check auth
        
        print(f"[DEBUG] Fetching papers for topic: {req.topic}")
        papers = fetch_papers(req.topic, max_results=req.max_results)

        if not papers:
            raise HTTPException(status_code=404, detail="No papers found.")

        if os.path.exists(INDEX_FILE):
            return {
                "message": "Papers already indexed",
                "status": "success",
                "papers": papers,
                "chunks": 0
            }

        print("[DEBUG] Processing papers...")
        chunks = load_and_process_papers()

        if not chunks:
            raise HTTPException(status_code=500, detail="Chunking failed.")

        print(f"[DEBUG] Creating vector store...")
        create_vector_store(chunks)

        return {
            "message": "Papers indexed successfully",
            "status": "success",
            "papers": papers,
            "chunks": len(chunks)
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/research_query")
def research_query(req: QueryRequest, authorization: str = Header(None)):
    """Query papers (requires auth)"""
    try:
        get_auth_token(authorization)  # Check auth
        
        print(f"[DEBUG] Query: {req.query}")

        if not os.path.exists(INDEX_FILE):
            raise HTTPException(status_code=404, detail="Vector store not found. Fetch papers first.")

        # Search
        results = search_vector_store(req.query, k=req.top_k)
        
        # Convert to chunks
        chunks = [
            Chunk(
                page_content=result["text"],
                metadata={"source": result["source"], "score": result["score"]}
            )
            for result in results
        ]

        # Generate answer
        answer_result = generate_answer(query=req.query, chunks=chunks)

        return JSONResponse(
            content={
                "query": req.query,
                "answer": answer_result.get("answer", ""),
                "research_gaps": answer_result.get("research_gaps", []),
                "sources": answer_result.get("sources", []),
                "status": "success"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    """Public health check"""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)