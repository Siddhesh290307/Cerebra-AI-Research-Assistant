#This files fetches relevant papers to user query
import arxiv
import os

SAVE_DIR = "papers"

#Searching arxiv, downloading pdfs, and returning paper metadata
def fetch_papers(query: str, max_results: int = 5) -> list[dict]:
    os.makedirs(SAVE_DIR, exist_ok=True)
    print(f"Searching arXiv for: '{query}'")

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    papers = []
    for result in search.results():
        paper_id = result.entry_id.split("/")[-1]
        pdf_path = os.path.join(SAVE_DIR, f"{paper_id}.pdf")
        # skipping already-downloaded papers
        if not os.path.exists(pdf_path):          
            print(f"  Downloading: {result.title}")
            result.download_pdf(filename=pdf_path)
        else:
            print(f"  Already exists, skipping: {result.title}")

        papers.append({
            "title": result.title,
            "summary": result.summary,
            "pdf_path": pdf_path,
            "authors": [a.name for a in result.authors]
        })

    print(f"Done. {len(papers)} paper(s) ready.")
    return papers