# chunk_model.py
# Simple wrapper class to make chunks compatible with both FAISS and LangChain

class Chunk:
    """Wrapper class for chunk data that behaves like LangChain Document"""
    
    def __init__(self, page_content: str, metadata: dict = None):
        self.page_content = page_content
        self.metadata = metadata or {}
    
    def __repr__(self):
        return f"Chunk(page_content='{self.page_content[:50]}...', metadata={self.metadata})"