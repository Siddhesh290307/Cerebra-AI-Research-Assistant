#This file embedds the given chunks
from langchain_huggingface import HuggingFaceEmbeddings

#embedding model from hugging face
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"  # 22MB, super fast
)