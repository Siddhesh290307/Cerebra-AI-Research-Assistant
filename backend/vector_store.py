# vector_store.py
# Uses FAISS to store vectors created from embeddings

import os
import pickle
import numpy as np
from embeddings import embedding_model

DB_PATH = "vector_store"
INDEX_FILE = os.path.join(DB_PATH, "faiss_index.pkl")
METADATA_FILE = os.path.join(DB_PATH, "metadata.pkl")


def _get_vector_dim() -> int:
    """Get embedding dimensions from the model"""
    test_embedding = embedding_model.embed_query("test")
    return len(test_embedding)


def _reset_database():
    """Reset the vector store folder"""
    try:
        if os.path.exists(DB_PATH):
            print(f"🔄 Resetting vector store at {DB_PATH}...")
            for file in os.listdir(DB_PATH):
                file_path = os.path.join(DB_PATH, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            print("✓ Vector store reset successfully")
    except Exception as e:
        print(f"⚠️  Warning: Could not reset vector store: {e}")


def create_vector_store(chunks: list) -> dict:
    """Embed chunks and store to FAISS"""
    try:
        if not chunks:
            raise ValueError("No chunks provided to create vector store")

        # Create database directory
        os.makedirs(DB_PATH, exist_ok=True)

        # Reset to avoid duplicates
        if os.path.exists(INDEX_FILE):
            _reset_database()

        print("[Vector Store] Creating FAISS vector store...")

        # Get embeddings for all chunks
        embeddings_list = []
        metadata_list = []

        for i, chunk in enumerate(chunks):
            print(f"  Embedding chunk {i+1}/{len(chunks)}...", end="\r")
            
            # Extract text from chunk (handle both string and object with page_content)
            text = chunk.page_content if hasattr(chunk, 'page_content') else str(chunk)
            
            # Create embedding
            embedding = embedding_model.embed_query(text)
            embeddings_list.append(embedding)
            
            # Store metadata
            metadata = {
                'text': text,
                'source': getattr(chunk, 'metadata', {}).get('source', 'unknown') if hasattr(chunk, 'metadata') else 'unknown'
            }
            metadata_list.append(metadata)

        print(" " * 50, end="\r")  # Clear progress line

        # Convert to numpy array
        embeddings_array = np.array(embeddings_list, dtype=np.float32)

        # Create and save FAISS index
        import faiss
        dimension = embeddings_array.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings_array)

        # Save index and metadata
        with open(INDEX_FILE, 'wb') as f:
            pickle.dump(index, f)
        
        with open(METADATA_FILE, 'wb') as f:
            pickle.dump(metadata_list, f)

        print(f"✓ Successfully indexed {len(chunks)} chunks into FAISS at '{DB_PATH}'.")
        return {
            'index': index,
            'metadata': metadata_list,
            'dimension': dimension
        }

    except Exception as e:
        print(f"✗ Error creating vector store: {str(e)}")
        raise


def load_vector_store() -> dict:
    """Load an existing FAISS index for querying"""
    try:
        if not os.path.exists(INDEX_FILE) or not os.path.exists(METADATA_FILE):
            raise RuntimeError(
                f"Vector store not found at '{DB_PATH}'. "
                f"Please call /fetch_papers endpoint first to create and index papers."
            )

        print("[Vector Store] Loading FAISS vector store...")
        
        with open(INDEX_FILE, 'rb') as f:
            index = pickle.load(f)
        
        with open(METADATA_FILE, 'rb') as f:
            metadata = pickle.load(f)

        print("✓ Successfully loaded FAISS vector store")
        return {
            'index': index,
            'metadata': metadata,
            'dimension': index.d
        }

    except Exception as e:
        print(f"✗ Error loading vector store: {str(e)}")
        raise


def search_vector_store(query: str, k: int = 5) -> list:
    """Search the vector store for similar chunks"""
    try:
        vector_store = load_vector_store()
        index = vector_store['index']
        metadata = vector_store['metadata']

        # Embed the query
        query_embedding = embedding_model.embed_query(query)
        query_array = np.array([query_embedding], dtype=np.float32)

        # Search
        distances, indices = index.search(query_array, k)

        # Format results
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(metadata):
                results.append({
                    'text': metadata[idx]['text'],
                    'source': metadata[idx]['source'],
                    'distance': float(distance),
                    'score': 1 / (1 + float(distance))  # Convert distance to similarity score
                })

        return results

    except Exception as e:
        print(f"✗ Error searching vector store: {str(e)}")
        raise