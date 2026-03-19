#This file splits the pdfs into sections so that they can be chunked accordingly
import re

SECTION_HEADERS = [
    "abstract", "introduction", "related work", "background",
    "method", "methods", "approach", "model",
    "experiments", "results", "discussion",
    "conclusion", "limitations", "future work"
]

_PATTERN = re.compile(
    r'(?im)^\s*(' + "|".join(re.escape(h) for h in SECTION_HEADERS) + r')\s*$'
)

#To split papers into sections
def split_into_sections(text: str) -> list[dict]:
    parts = _PATTERN.split(text)

    if len(parts) < 3:
        return [{"section": "full_text", "text": text}]

    sections = []
    for i in range(1, len(parts) - 1, 2):
        body = parts[i + 1].strip()
        if body:
            sections.append({"section": parts[i].strip().lower(), "text": body})

    return sections or [{"section": "full_text", "text": text}]