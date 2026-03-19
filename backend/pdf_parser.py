#extracting and returning all text from a pdf file.
import fitz  


def extract_text(pdf_path: str) -> str:
    with fitz.open(pdf_path) as doc:
        return "".join(page.get_text() for page in doc)


if __name__ == "__main__":
    sample = "papers/2402.04563v1.pdf"
    text = extract_text(sample)
    print(f"Characters extracted: {len(text)}")
    print(text[:500])