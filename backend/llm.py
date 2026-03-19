#This file gives relevant chunks to groq and returns the answer given by it
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY not set properly")

import json

def safe_json_parse(text: str):
    text = text.strip()

    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]

    try:
        return json.loads(text)
    except:
        return []


def categorize_question(query: str, context: str) -> str:
    """
    Categorize question as 'known' or 'unknown'
    known = directly answerable from papers
    unknown = needs reasoning beyond papers
    """
    try:
        categorize_prompt = f"""
Categorize this question as either 'known' or 'unknown':

KNOWN = The answer can be directly found or clearly inferred from research papers
UNKNOWN = The answer requires broader ML reasoning beyond what papers discuss

Context snippets:
{context[:500]}...

Question:
{query}

Respond ONLY with: known or unknown
"""
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": categorize_prompt}],
            temperature=0.1,
            max_tokens=10
        )
        category = response.choices[0].message.content.strip().lower()
        return "known" if "known" in category else "unknown"
    except:
        return "unknown"


def generate_answer(query: str, chunks: list, mode: str = "grounded") -> dict:
    """
    Modes:
    - speculative → no context, pure reasoning
    - hybrid → weak context + reasoning
    - grounded → normal RAG
    - grounded_strict → strict citation
    """

    # -------------------------------
    # Context Prep
    # -------------------------------
    seen = set()
    context_items = []
    paper_map = {}

    for chunk in chunks:
        text = chunk.page_content.strip()

        if text[:200] in seen:
            continue
        seen.add(text[:200])

        paper = chunk.metadata.get("paper", "Unknown")
        section = chunk.metadata.get("section", "Unknown")

        paper_map[paper] = True

        context_items.append(
            f"[Source {len(context_items)+1}: {paper} - {section}]\n{text}"
        )

        if len(context_items) >= 6:
            break

    context = "\n\n---\n\n".join(context_items)

    # 🔥 Categorize question as known or unknown
    question_category = categorize_question(query, context)

    # 🔥 Force speculative if context empty
    if not context.strip():
        question_category = "unknown"

    # -------------------------------
    # PROMPT BASED ON CATEGORY
    # -------------------------------
    if question_category == "known":
        # EXPAND A LOT - deep dive into papers
        prompt = f"""
You are a research scientist analyzing papers on this topic.

The question is DIRECTLY ANSWERABLE from the papers.

Context:
{context}

Question:
{query}

INSTRUCTIONS:
- Expand comprehensively on what the papers say
- Explain the mechanisms and reasoning in detail
- For related smaller concepts mentioned in papers, explain them briefly
- Go deep: discuss trade-offs, limitations, improvements
- Cite specific findings and numbers from context
- Be confident and thorough - this is grounded knowledge

Provide a detailed, technical answer that fully explores what the papers discuss.
"""

    else:  # unknown
        # USE OWN BRAIN - but try to link to papers
        prompt = f"""
You are a research scientist.

The question extends beyond what the papers directly discuss.

Context:
{context}

Question:
{query}

INSTRUCTIONS:
- Use your ML knowledge and reasoning
- Try to link your reasoning to the papers when possible
- If papers discuss related concepts, build on them
- If papers don't directly address this, be honest and reason from first principles
- Answer YES or NO with justification if it's a binary question
- Be technical and specific, not generic
- Explain the reasoning clearly

Provide your best answer using papers as foundation + your own reasoning.
"""

    # -------------------------------
    # Answer Generation (safe)
    # -------------------------------
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4 if question_category == "known" else 0.5,
            max_tokens=4000
        )
        answer_text = response.choices[0].message.content.strip()
    except Exception as e:
        answer_text = f"Model failed to generate a response. {e}"

    # -------------------------------
    # Insights (STRICT FORMAT 🔥)
    # -------------------------------
    insights = []

    insight_prompt = f"""
Generate EXACTLY 3 high-quality research ideas.

STRICT RULES:
- Each idea MUST include:
  1. hypothesis
  2. mechanism
  3. metric (how to measure)
  4. experiment (clear setup)

- Reject vague ideas
- Reject high-level studies
- Use technical language
- If not measurable → discard

Question:
{query}

Return JSON:
[
  {{
    "hypothesis": "...",
    "mechanism": "...",
    "metric": "...",
    "experiment": "..."
  }}
]
"""

    try:
        insight_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": insight_prompt}],
            temperature=0.5,
            max_tokens=600
        )

        insights_raw = safe_json_parse(insight_response.choices[0].message.content)

        if isinstance(insights_raw, list):
            # enforce structure
            for idea in insights_raw[:3]:
                if all(k in idea for k in ["hypothesis", "mechanism", "metric", "experiment"]):
                    insights.append(idea)

    except Exception:
        insights = []

    # -------------------------------
    # Sources
    # -------------------------------
    unique_sources = []
    seen_sources = set()

    for chunk in chunks:
        key = (
            chunk.metadata.get("paper", ""),
            chunk.metadata.get("section", "")
        )
        if key not in seen_sources:
            seen_sources.add(key)
            unique_sources.append({
                "paper": key[0],
                "section": key[1]
            })

    return {
        "answer": answer_text,
        "research_gaps": insights,
        "sources": unique_sources
    }