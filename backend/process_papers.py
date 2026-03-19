#This file processes all the pdfs
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from pdf_parser import extract_text
from section_splitter import split_into_sections
from chunker import semantic_chunk_section

PAPER_DIR = "papers"
MAX_WORKERS = 4


def _process_single_paper(filename: str) -> list:
    path = os.path.join(PAPER_DIR, filename)
    text = extract_text(path)
    sections = split_into_sections(text)

    chunks = []
    for sec in sections:
        chunks.extend(
            semantic_chunk_section(sec["text"], sec["section"], filename)
        )
    return chunks

#parses, section wise splits, and semantically chunks every pdf in PAPER_DIR in parallel
def load_and_process_papers() -> list:
    pdf_files = [f for f in os.listdir(PAPER_DIR) if f.endswith(".pdf")]

    if not pdf_files:
        print("No PDFs found in", PAPER_DIR)
        return []

    print(f"Processing {len(pdf_files)} PDFs.")
    all_chunks = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(_process_single_paper, f): f for f in pdf_files}
        for future in as_completed(futures):
            filename = futures[future]
            try:
                chunks = future.result()
                all_chunks.extend(chunks)
                print(f"{filename}: {len(chunks)} chunks")
            except Exception as e:
                print(f"{filename} failed: {e}")

    print(f"\nTotal chunks: {len(all_chunks)}")
    return all_chunks


if __name__ == "__main__":
    chunks = load_and_process_papers()
    for c in chunks[:5]:
        print(f"\n[{c.metadata['section']}] {c.metadata['paper']}")
        print(c.page_content[:200])