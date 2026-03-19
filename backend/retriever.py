# retriever.py
# Wrapper for vector store search operations

from vector_store import search_vector_store
from chunk_model import Chunk

def search(query: str, k: int = 6):
    """
    Search the vector store and return results in chunk format
    
    Args:
        query: Search query string
        k: Number of results to return
        
    Returns:
        List of Chunk objects with page_content and metadata
    """
    try:
        print(f"[Retriever] Searching for: {query}")
        
        # Get results from FAISS
        results = search_vector_store(query, k=k)
        
        # Convert to Chunk objects for compatibility with llm.py
        chunks = [
            Chunk(
                page_content=result["text"],
                metadata={
                    "source": result["source"],
                    "similarity_score": result["score"],
                    "distance": result["distance"]
                }
            )
            for result in results
        ]
        
        print(f"[Retriever] Found {len(chunks)} relevant chunks")
        return chunks
        
    except Exception as e:
        print(f"[Retriever] Error during search: {str(e)}")
        raise