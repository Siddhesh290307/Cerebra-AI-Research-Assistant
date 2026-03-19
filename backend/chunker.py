#This file creates sematic chunks sectionwise
from langchain_experimental.text_splitter import SemanticChunker
from langchain_core.documents import Document
from embeddings import embedding_model

semantic_splitter = SemanticChunker(
    embedding_model,
    breakpoint_threshold_type="percentile", 
    breakpoint_threshold_amount=85
)

#Semantically chunking a paper section into langchain documents
def semantic_chunk_section(section_text: str, section_name: str, paper_title: str) -> list[Document]:
    docs = semantic_splitter.create_documents([section_text])
    return [
        Document(
            page_content=doc.page_content,
            metadata={"section": section_name, "paper": paper_title}
        )
        for doc in docs
    ]