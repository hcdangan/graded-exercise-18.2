"""MCP stdio server for the fictional market corpus."""
import csv
import re
from pathlib import Path
from mcp.server.fastmcp import FastMCP

ROOT = Path(__file__).resolve().parent
server = FastMCP("Week 18 fictional market corpus")

@server.resource("corpus://market/corpus.csv")
def corpus() -> str:
    return (ROOT / "data/corpus.csv").read_text(encoding="utf-8")

@server.resource("corpus://market/glossary.md")
def glossary() -> str:
    return (ROOT / "data/glossary.md").read_text(encoding="utf-8")

@server.tool()
def search_corpus(query: str, limit: int = 5) -> list[dict[str, str]]:
    """Find matching paragraphs by case-insensitive keyword overlap; return cited snippets."""
    if not 1 <= limit <= 12:
        raise ValueError("limit must be between 1 and 12")
    words = set(re.findall(r"[a-z0-9]+", query.lower())) - {"the", "and", "in", "of", "a", "to", "assess"}
    with (ROOT / "data/corpus.csv").open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    scored = [(len(words & set(re.findall(r"[a-z0-9]+", row["text"].lower()))), row) for row in rows]
    scored.sort(key=lambda pair: (-pair[0], pair[1]["id"]))
    return [{"text": row["text"], "source": row["id"]} for score, row in scored if score][:limit]

if __name__ == "__main__":
    server.run(transport="stdio")
